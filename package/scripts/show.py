#!/usr/bin/env python3

import wx
import sys
import pickle
from threading import Thread


class Listener(Thread):
    """Listener Thread Class"""

    def __init__(self, notifyWindow):
        Thread.__init__(self)
        self.notifyWindow = notifyWindow
        self.daemon = True
        self.start()

    def run(self):
        while True:
            try:
                # Blocking read: Wait until there's control byte data
                control = sys.stdin.buffer.read(1)
                if not control:
                    # Blocked read and there is no control byte, keep waiting
                    continue

                if control == bytes([0]):
                    wx.CallAfter(self.notifyWindow.on_shutdown)
                    return
                elif control == bytes([1]):
                    # Read the picture data size (next 8 bytes)
                    size_bytes = sys.stdin.buffer.read(8)
                    size = int.from_bytes(size_bytes, byteorder='big')
                    if size == 0:
                        continue
                    payload = sys.stdin.buffer.read(size)
                    wx.CallAfter(self.notifyWindow.on_new_picture, payload)
                else:
                    print("Unexpected control byte", file=sys.stderr)
            except Exception as e:
                print(f"Listener error: {e}", file=sys.stderr)
                break


class MainWindow(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent=parent, title="Image Viewer", size=(400, 400))
        self.panel = wx.Panel(self)
        self.imageCtrl = None  # this will hold the image

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.sizer)

        self.listener = Listener(self)

        self.Show()

    def on_shutdown(self):
        self.Close()

    def on_new_picture(self, pickled_picture):
        try:
            picture = pickle.loads(pickled_picture)
            self.update_bitmap(picture)
        except Exception as e:
            print(f"Error loading picture: {e}", file=sys.stderr)

    def update_bitmap(self, picture):
        wx_image = picture.getWxImage()
        bitmap = wx.Bitmap(wx_image)

        # Clear old image
        if self.imageCtrl:
            self.imageCtrl.Destroy()

        self.imageCtrl = wx.StaticBitmap(self.panel, bitmap=bitmap)

        # Update window title
        self.SetTitle(picture.getTitle())

        # Refit layout
        self.sizer.Clear(True)
        self.sizer.Add(self.imageCtrl, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        self.panel.Layout()
        self.Fit()
        self.Center()


def main():
    app = wx.App(False)
    frame = MainWindow(parent=None)
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
