#!/usr/bin/env python3

import os
import sys
import wx
import wx.lib.scrolledpanel

class Cursor:
    width  = 7
    height = 7
    centerX = int((width - 1)/2)
    centerY = int((height - 1)/2)
    cursorBitmap = None
    savedCursorPosition = None
    cursorBackupBitmap = None

    def __init__(self, width=7, height=7):
        self.width = width
        self.height = height
        self.centerX = int((self.width - 1)/2)
        self.centerY = int((self.height - 1)/2)

        if wx.Platform != "__WXMAC__":
            dc = wx.MemoryDC()

            cursorMask = wx.Bitmap(self.width, self.height, depth=1)
            dc.SelectObject(cursorMask)
            dc.SetPen(wx.Pen(wx.Colour(255, 255, 255), width=3))
            dc.DrawLine(0, self.centerY, self.width-1, self.centerY)
            dc.DrawLine(self.centerX, 0, self.centerX, self.height-1)

            self.cursorBitmap = wx.Bitmap(self.width, self.height)
            dc.SelectObject(self.cursorBitmap)
            dc.SetPen(wx.Pen(wx.Colour(255, 255, 0)))
            dc.DrawLine(0, self.centerY, self.width-1, self.centerY)
            dc.DrawLine(self.centerX, 0, self.centerX, self.height-1)
            self.cursorBitmap.SetMask(wx.Mask(cursorMask))

            del dc

    def drawCursor(self, canvas, x, y):
        W, H = canvas.image.GetSize()
        W, H = int(W * canvas.zoomFactor), int(H * canvas.zoomFactor)

        w, h = self.width, self.height
        dx, dy = self.centerX, self.centerY
        x0 = max(0, x-dx)
        y0 = max(0, y-dy)
        w0 = dx + min(dx+1, W-x)
        h0 = dy + min(dy+1, H-y)
        cursorRect = wx.Rect(x0, y0, w0, h0)
        cursorPosition = x-dx, y-dy
        self.savedCursorPosition = x0, y0
        self.cursorBackupBitmap = canvas.bmp.GetSubBitmap(cursorRect)

        if wx.Platform == "__WXMSW__":
            dc = wx.ClientDC(canvas.imageCtrl)
        else:
            dc = wx.ClientDC(canvas.imagePanel)
            canvas.imagePanel.DoPrepareDC(dc)
        dc.SetClippingRegion(0, 0, W, H)
        if self.cursorBitmap is None:
            dx, dy = self.centerX-1, self.centerY-1
            dc.SetPen(wx.Pen(wx.Colour(0, 0, 0), width=3))
            dc.DrawLine(x-dx, y, x+dx, y)
            dc.DrawLine(x, y-dy, x, y+dy)
            dc.SetPen(wx.Pen(wx.Colour(255, 255, 0), width=1))
            dc.DrawLine(x-dx, y, x+dx, y)
            dc.DrawLine(x, y-dy, x, y+dy)
        else:
            dc.DrawBitmap(self.cursorBitmap, cursorPosition, True)
        del dc

    def undrawPreviousCursor(self, canvas):
        """Restore bitmap (if any) saved from previous cursor event
        """
        if self.cursorBackupBitmap is not None:
            if wx.Platform == "__WXMSW__":
                dc = wx.ClientDC(canvas.imageCtrl)
            else:
                dc = wx.ClientDC(canvas.imagePanel)
                canvas.imagePanel.DoPrepareDC(dc)
            dc.DrawBitmap(self.cursorBackupBitmap, self.savedCursorPosition, False)
            del dc

    def drawCrosshairs(self, canvas):
        """Draw image with crosshairs to indicate selected position
        """
        x = int(int(canvas.pixelTxtX.GetValue()) * canvas.zoomFactor)
        y = int(int(canvas.pixelTxtY.GetValue()) * canvas.zoomFactor)

        self.undrawPreviousCursor(canvas)
        self.drawCursor(canvas, x, y)

    def clearBackupBitmap(self):
        """Forget saved bitmap buffer
        """
        if self.cursorBackupBitmap is not None:
            self.cursorBackupBitmap = None

class MainWindow(wx.Frame):

    MinWindowWidth = 350
    MinWindowHeight = 0
    ColorPanelHeight = 70
    PaintChipSize = 24
    zoomLevels = [25, 50, 75, 100, 150, 200, 500]
    zoomFactor = float(zoomLevels[3]) / 100.0
    cursorSize = (7, 7)
    cursorBitmap = None
    x = 0
    y = 0

    def __init__(self, filename, parent, title):
        self.image = wx.Image(filename, wx.BITMAP_TYPE_ANY)
        self.bmp = wx.Bitmap(self.image)
        super(MainWindow, self).__init__(parent=parent, title=title, style=wx.DEFAULT_FRAME_STYLE)

        self.InitUI()
        self.Center()
        self.clipOnBoundary()

    def InitUI(self):
        wView, hView = wx.DisplaySize()
        wView, hView = int(wView * 0.95), int(hView * 0.85)

        w, h = self.image.GetSize()
        w = min(max(self.MinWindowWidth, w), wView)
        h = min(max(self.MinWindowHeight, h + self.ColorPanelHeight), hView)

        self.setupZoomMenu()

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.setupColorInfoDisplay()
        self.mainSizer.Add(self.colorInfoPanel, 0, wx.EXPAND|wx.ALL, 0)

        self.setupImageDisplay()
        self.mainSizer.Add(self.imagePanel, 0, wx.EXPAND|wx.ALL, 0)
        self.SetSizer(self.mainSizer)
        self.Fit()

        self.SetSize((w, h))
        self.SetClientSize((w,h))

    def setupZoomMenu(self):
        zoomMenu = wx.Menu()
        for z in self.zoomLevels:
            item = "{}%".format(z)
            helpString = "Zoom by {}%".format(z)
            zoomID = zoomMenu.Append(wx.ID_ANY, item, helpString)
            self.Bind(wx.EVT_MENU, self.onZoom, zoomID)

        menuBar = wx.MenuBar()
        menuBar.Append(zoomMenu, "&Zoom") 
        self.SetMenuBar(menuBar) 

    def setupColorInfoDisplay(self):
        self.colorInfoPanel = wx.Panel(parent=self, size=(-1, self.ColorPanelHeight))

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        sizer1 = wx.BoxSizer(wx.HORIZONTAL)

        lblX = wx.StaticText(self.colorInfoPanel, 0, style=wx.ALIGN_CENTER)
        lblY = wx.StaticText(self.colorInfoPanel, 0, style=wx.ALIGN_CENTER)
        lblX.SetLabel("X: ")
        lblY.SetLabel("Y: ")

        img_R = os.path.join(sys.path[0], 'images', 'Right.png')
        img_L = os.path.join(sys.path[0], 'images', 'Left.png')
        bmp_R = wx.Bitmap(img_R, wx.BITMAP_TYPE_ANY)
        bmp_L = wx.Bitmap(img_L, wx.BITMAP_TYPE_ANY)
        bmp_size = (bmp_L.GetWidth()+5,bmp_L.GetHeight()+5)
        buttonX_L = wx.BitmapButton(self.colorInfoPanel, wx.ID_ANY, bitmap=bmp_L, size=bmp_size)
        buttonX_L.myname = "XL"
        buttonX_R = wx.BitmapButton(self.colorInfoPanel, wx.ID_ANY, bitmap=bmp_R, size=bmp_size)
        buttonX_R.myname = "XR"
        buttonY_L = wx.BitmapButton(self.colorInfoPanel, wx.ID_ANY, bitmap=bmp_L, size=bmp_size)
        buttonY_L.myname = "YL"
        buttonY_R = wx.BitmapButton(self.colorInfoPanel, wx.ID_ANY, bitmap=bmp_R, size=bmp_size)
        buttonY_R.myname = "YR"
        buttonX_L.Bind(wx.EVT_BUTTON, self.ImageCtrl_OnNavBtn)
        buttonX_R.Bind(wx.EVT_BUTTON, self.ImageCtrl_OnNavBtn)
        buttonY_L.Bind(wx.EVT_BUTTON, self.ImageCtrl_OnNavBtn)
        buttonY_R.Bind(wx.EVT_BUTTON, self.ImageCtrl_OnNavBtn)

        self.pixelTxtX = wx.TextCtrl(self.colorInfoPanel, wx.ALIGN_CENTER,
            style=wx.TE_PROCESS_ENTER, size=(50, -1))
        self.pixelTxtY = wx.TextCtrl(self.colorInfoPanel, wx.ALIGN_CENTER,
            style=wx.TE_PROCESS_ENTER, size=(50, -1))
        self.pixelTxtX.Bind(wx.EVT_TEXT_ENTER, self.ImageCtrl_OnEnter)
        self.pixelTxtY.Bind(wx.EVT_TEXT_ENTER, self.ImageCtrl_OnEnter)

        sizer1.Add(lblX, 0, flag=wx.CENTER, border=0) 
        sizer1.Add(buttonX_L, 0, border=0)
        sizer1.Add(self.pixelTxtX, 0, flag=wx.CENTER, border=5) 
        sizer1.Add(buttonX_R, 0, border=0)
        sizer1.Add((5, -1)) 
        sizer1.Add(lblY, 0, flag=wx.CENTER, border=0)
        sizer1.Add(buttonY_L, 0, border=0)
        sizer1.Add(self.pixelTxtY, 0, flag=wx.CENTER, border=5) 
        sizer1.Add(buttonY_R, 0, border=0)
        
        mainSizer.Add(sizer1, 0, flag=wx.LEFT|wx.RIGHT|wx.TOP|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, border=1)
        mainSizer.Add((-1, 5)) 
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)


        self.rgbValue = wx.StaticText(self.colorInfoPanel, label=u'')
        font = self.rgbValue.GetFont()
        font.PointSize += 2
        self.rgbValue.Font = font


        bmp = wx.Bitmap(self.PaintChipSize, self.PaintChipSize)
        self.colorPreview = wx.StaticBitmap(parent=self.colorInfoPanel, bitmap=bmp)

        sizer2.Add(self.rgbValue, 0, flag=wx.ALIGN_CENTER, border=5)
        sizer2.Add((10, -1), 0) 

        sizer2.Add(self.colorPreview, 0, flag=wx.ALIGN_CENTER, border=5) 

        mainSizer.Add(sizer2, 0, flag=wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, border=1)
        mainSizer.Add((-1, 5))

        self.colorInfoPanel.SetSizer(mainSizer)

    def setupImageDisplay(self):
        """Set up image display panel
        """

        w, h = self.image.GetSize()
        maxZoomLevel = int(int(self.zoomLevels[-1]) / 100)
        maxSize = (maxZoomLevel * w, maxZoomLevel * h)
    
        self.imagePanel = wx.lib.scrolledpanel.ScrolledPanel(parent=self, size=maxSize, style=wx.NO_BORDER)

        self.imageCtrl = wx.StaticBitmap(parent=self.imagePanel, bitmap=self.bmp)
        if wx.Platform == "__WXMSW__" or wx.Platform == "__WXGTK__":
            self.imageCtrl.Bind(wx.EVT_LEFT_DOWN, self.ImageCtrl_OnMouseClick)
            self.imageCtrl.Bind(wx.EVT_MOTION, self.ImageCtrl_OnMouseClick)
        elif wx.Platform == "__WXMAC__":
            self.imagePanel.Bind(wx.EVT_LEFT_DOWN, self.ImageCtrl_OnMouseClick)
            self.imagePanel.Bind(wx.EVT_MOTION, self.ImageCtrl_OnMouseClick) 

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.imageCtrl, 0, wx.ALIGN_LEFT|wx.ALIGN_TOP|wx.ALL, 0)
        self.imagePanel.SetSizer(mainSizer)
        self.mainSizer.Fit(self.imagePanel)
        self.imagePanel.SetupScrolling(scrollToTop=True)

        self.crosshair = Cursor()

    def clipOnBoundary(self):
        """Clips x and y to be valid pixel coordinates

        Ensures that the current values of x and y are valid pixel
        coordinates for the image

        Modifies
        --------
        self.x, self.y : int
            the pixel coordinates
        self.pixelTxtX, self.pixelTxtY : wx.TextCtrl
            the textboxes displaying the pixel coordinates
        """
        width, height = self.image.GetSize()
        if self.x < 0:
            self.x = 0
        elif self.x >= width:
            self.x = width - 1
        if self.y < 0:
            self.y = 0
        elif self.y >= height:
            self.y = height - 1
        self.pixelTxtX.SetValue(str(self.x))
        self.pixelTxtY.SetValue(str(self.y))
        self.updateColorInfo()

    def updateColorInfo(self):
        """Updates the color patch in the color information display

        The color patch is a small square image with a black outline and
        interior color matching that corresponding to the most-recently
        selected pixel in the image.
        """
        r = self.image.GetRed(self.x, self.y)
        g = self.image.GetGreen(self.x, self.y)
        b = self.image.GetBlue(self.x, self.y)
        self.rgbValue.SetLabel(label=u'R: {} G: {} B: {}  Color at location:'.format(r, g, b))

        bmp = wx.Bitmap(self.PaintChipSize, self.PaintChipSize)
        dc = wx.MemoryDC()
        dc.SelectObject(bmp)
        dc.SetPen(wx.Pen(wx.Colour(0,0,0))) 
        dc.SetBrush(wx.Brush(wx.Colour(r,g,b))) 
        dc.DrawRectangle(0, 0, self.PaintChipSize, self.PaintChipSize)
        del dc
        self.colorPreview.SetBitmap(bmp) 
        self.colorInfoPanel.Layout()

    def updateView(self):
        """Scale image according to the zoom factor and (re)display it
        """
        w, h = self.image.GetSize()
        w, h = int(w * self.zoomFactor), int(h * self.zoomFactor)
        image = self.image.Scale(w, h)
        self.bmp = wx.Bitmap(image)
        self.imageCtrl.SetBitmap(self.bmp)

        self.crosshair.clearBackupBitmap()
        
    def drawCrosshairs(self):
        """Draw image with crosshairs to indicate selected position
        """
        self.crosshair.drawCrosshairs(self)

# ===========================================================================
# Event handlers
# ===========================================================================

    def onFocus(self, event):
        self.imagePanel.SetFocus()

    def onZoom(self, event):
        """Sets desired zoom level and updates image display
        """
        id_selected = event.GetId() 
        obj = event.GetEventObject() 
        menuItem = obj.GetLabelText(id_selected)
        self.zoomFactor = float(menuItem.replace('%','')) / 100.0

        self.imagePanel.Scroll(0, 0) 

        self.PostSizeEvent()
        self.clipOnBoundary()
        self.updateView()

    def ImageCtrl_OnNavBtn(self, event):
        """Increment or decrement x or y pixel coordinate
        """
        selectedBtn = event.GetEventObject().myname
        if selectedBtn == "XL":
            self.x = int(self.pixelTxtX.GetValue()) - 1
        elif selectedBtn == "XR":
            self.x = int(self.pixelTxtX.GetValue()) + 1
        elif selectedBtn == "YL":
            self.y = int(self.pixelTxtY.GetValue()) - 1
        elif selectedBtn == "YR":
            self.y = int(self.pixelTxtY.GetValue()) + 1
        self.clipOnBoundary()
        self.drawCrosshairs()

    def ImageCtrl_OnEnter(self, event):
        """Adjusts x and y pixel values to match displayed values
        """
        self.x = int(self.pixelTxtX.GetValue())
        self.y = int(self.pixelTxtY.GetValue())
        self.clipOnBoundary()
        self.drawCrosshairs()

    def ImageCtrl_OnMouseClick(self, event):
        """Update x and y pixel coordinates from pointer location
        """
        if event.LeftIsDown():
            event.Skip()
            if wx.Platform == "__WXMSW__":
                cursorPosition = event.GetPosition()
            elif wx.Platform == "__WXGTK__" or wx.Platform == "__WXMAC__":
                dc = wx.ClientDC(self)
                self.imagePanel.DoPrepareDC(dc)
                cursorPosition = event.GetLogicalPosition(dc)
                del dc

            self.x = int(cursorPosition.x / self.zoomFactor)
            self.y = int(cursorPosition.y / self.zoomFactor)

            self.clipOnBoundary()
            self.drawCrosshairs()

# ===========================================================================
# Main program
# ===========================================================================

def main(argv):

    usage = "usage: {} file [title]".format(argv[0])
    if len(argv) == 2:
        filename = title = argv[1]
    elif len(argv) == 3:
        filename = argv[1]
        title = argv[2]
    else:
        print(usage)
        exit(1)

    if not os.path.isfile(filename):
        print("{} does not exist or is not a file".format(filename))
        print(usage)
        exit(1)

    app = wx.App(False)
    frame = MainWindow(filename=filename, parent=None, title=title)
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main(sys.argv)
