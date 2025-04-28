#!/usr/bin/env python3

import os
import sys
import wx
import wx.lib.scrolledpanel


class MainWindow(wx.Frame):
    MinWindowWidth = 300
    MinWindowHeight = 300

    def __init__(self, filename, parent, title="Image Viewer"):
        # Load image and get image size
        self.image = wx.Image(filename, wx.BITMAP_TYPE_ANY)
        self.bmp = wx.Bitmap(self.image)
        super(MainWindow, self).__init__(parent=parent, title=title, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

        self.InitUI()
        self.Center()

    def InitUI(self):
        w, h = self.image.GetSize()

        # Set up main panel
        self.imagePanel = wx.Panel(self)

        # Create StaticBitmap to show the image
        self.imageCtrl = wx.StaticBitmap(self.imagePanel, bitmap=self.bmp)

        # Create sizer to center the image
        sizer = wx.BoxSizer(wx.VERTICAL)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)

        # Center horizontally and vertically
        hSizer.Add(self.imageCtrl, 0, wx.ALIGN_CENTER)
        sizer.Add(hSizer, 1, wx.ALIGN_CENTER)

        self.imagePanel.SetSizer(sizer)

        # Apply sizer to frame
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer.Add(self.imagePanel, 1, wx.EXPAND)
        self.SetSizer(self.mainSizer)

        # Set minimum client size
        self.SetMinSize((self.MinWindowWidth, self.MinWindowHeight))

        # Set initial window size: either image size or minimum
        initialW = max(w, self.MinWindowWidth)
        initialH = max(h, self.MinWindowHeight)
        self.SetClientSize((initialW, initialH))

# ===========================================================================
# Main program
# ===========================================================================

def main(argv):
    usage = "usage: {} file [title]".format(argv[0])
    # Get image file name and optional image title from command line
    if len(argv) == 2:
        filename = argv[1]
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
    frame = MainWindow(filename=filename, parent=None)
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main(sys.argv)
