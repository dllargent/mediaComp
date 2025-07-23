#!/usr/bin/env python3

import wx
import sys
import pickle
from threading import Thread, Event
import traceback
import os
import select
import time

script_dir = os.path.dirname(os.path.abspath(__file__))  
package_dir = os.path.dirname(script_dir)  
parent_dir = os.path.dirname(package_dir) 

for path in [parent_dir, package_dir]:
    if path not in sys.path:
        sys.path.insert(0, path)

package_imported = False
try:
    from mediaComp import *
    package_imported = True
except ImportError:
    try:
        sys.path.insert(0, package_dir)
        from mediaComp.core import *
        from mediaComp.models import *
        package_imported = True
    except ImportError:
        try:
            from mediaComp.core import *
            from mediaComp.models import *
            package_imported = True
        except ImportError as e:
            print(f"Warning: Could not import package modules: {e}", file=sys.stderr)
            print(f"Script directory: {script_dir}", file=sys.stderr)
            print(f"Package directory: {package_dir}", file=sys.stderr)
            print(f"Parent directory: {parent_dir}", file=sys.stderr)
            print(f"Current working directory: {os.getcwd()}", file=sys.stderr)
            print(f"Python path: {sys.path}", file=sys.stderr)


class Listener(Thread):
    """Listener Thread Class with proper cleanup"""

    def __init__(self, notifyWindow):
        Thread.__init__(self)
        self.notifyWindow = notifyWindow
        self.daemon = True
        self._stop_event = Event()
        self._running = True
        self.start()

    def run(self):
        try:
            while self._running and not self._stop_event.is_set():
                try:
                    # Use select to check if data is available (Unix/Linux/Mac)
                    if hasattr(select, 'select'):
                        ready, _, _ = select.select([sys.stdin], [], [], 0.1)
                        if not ready:
                            continue
                    
                    # Set stdin to non-blocking mode temporarily
                    control = sys.stdin.buffer.read(1)
                    if not control:
                        if not self._stop_event.is_set():
                            wx.CallAfter(self.notifyWindow.on_program_ended)
                        break
                    
                    if control == bytes([0]):
                        if not self._stop_event.is_set():
                            wx.CallAfter(self.notifyWindow.on_shutdown)
                        break
                    elif control == bytes([1]):
                        size_bytes = sys.stdin.buffer.read(8)
                        if len(size_bytes) < 8:
                            print("Incomplete size data received", file=sys.stderr)
                            break
                        
                        size = int.from_bytes(size_bytes, byteorder='big')
                        
                        if size == 0:
                            continue
                        
                        payload = b''
                        bytes_read = 0
                        while bytes_read < size and not self._stop_event.is_set():
                            chunk = sys.stdin.buffer.read(min(4096, size - bytes_read))
                            if not chunk:
                                print("Incomplete payload data received", file=sys.stderr)
                                break
                            payload += chunk
                            bytes_read += len(chunk)
                        
                        if len(payload) == size and not self._stop_event.is_set():
                            wx.CallAfter(self.notifyWindow.on_new_picture, payload)
                        elif not self._stop_event.is_set():
                            print(f"Payload size mismatch: expected {size}, got {len(payload)}", file=sys.stderr)
                    else:
                        print(f"Unexpected control byte: {control[0]}", file=sys.stderr)
                        
                except EOFError:
                    print("EOF in listener thread - program ended", file=sys.stderr)
                    if not self._stop_event.is_set():
                        wx.CallAfter(self.notifyWindow.on_program_ended)
                    break
                except OSError as e:
                    # Handle broken pipe or other OS errors gracefully
                    if e.errno == 32:  # Broken pipe
                        print("Broken pipe - parent process ended", file=sys.stderr)
                    else:
                        print(f"OS error in listener: {e}", file=sys.stderr)
                    break
                except Exception as e:
                    if not self._stop_event.is_set():
                        print(f"Listener error: {e}", file=sys.stderr)
                        traceback.print_exc(file=sys.stderr)
                    break
        except Exception as e:
            print(f"Listener thread exception: {e}", file=sys.stderr)
        finally:
            print("Listener thread ending", file=sys.stderr)

    def stop(self):
        """Signal the thread to stop and wait for it to finish"""
        self._running = False
        self._stop_event.set()
        
        # Give the thread a chance to finish gracefully
        if self.is_alive():
            self.join(timeout=1.0)  # Wait up to 1 second
            if self.is_alive():
                print("Warning: Listener thread did not stop gracefully", file=sys.stderr)


class MainWindow(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent=parent, title="Image Viewer", 
                        style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        
        self.panel = wx.Panel(self)
        self.imageCtrl = None  
        self.listener = None

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.sizer)

        self.placeholder = wx.StaticText(self.panel, label="Waiting for image...")
        self.sizer.Add(self.placeholder, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        self.SetClientSize((300, 100))
        self.Center()

        # Start the listener thread
        self.listener = Listener(self)

        # Bind close event
        self.Bind(wx.EVT_CLOSE, self.on_close)
        
        # Also bind to window destroy to ensure cleanup
        self.Bind(wx.EVT_WINDOW_DESTROY, self.on_destroy)

        self.Show()

    def on_close(self, event):
        """Handle window close event"""
        print("Window closing...", file=sys.stderr)
        self.cleanup_listener()
        
        # Allow the window to close
        event.Skip()

    def on_destroy(self, event):
        """Handle window destroy event"""
        print("Window being destroyed...", file=sys.stderr)
        self.cleanup_listener()
        event.Skip()

    def cleanup_listener(self):
        """Clean up the listener thread"""
        if hasattr(self, 'listener') and self.listener is not None:
            print("Stopping listener thread...", file=sys.stderr)
            self.listener.stop()
            self.listener = None

    def on_program_ended(self):
        """Called when the program that's sending data ends"""
        self.cleanup_listener()
        
        current_title = self.GetTitle()
        if not current_title.endswith(" - Complete"):
            self.SetTitle(current_title + " - Complete")

    def on_shutdown_signal(self):
        """Called when shutdown signal is received"""
        self.cleanup_listener()
        
        current_title = self.GetTitle()
        if not current_title.endswith(" - Complete"):
            self.SetTitle(current_title + " - Complete")

    def on_shutdown(self):
        """Called to shutdown the application"""
        self.cleanup_listener()
        wx.CallAfter(self.Close)

    def on_new_picture(self, pickled_picture):
        try:            
            picture = pickle.loads(pickled_picture)
            self.update_bitmap(picture)
            
        except ModuleNotFoundError as e:
            print(f"ModuleNotFoundError during unpickling: {e}", file=sys.stderr)
            print("This usually means the 'package' module cannot be found.", file=sys.stderr)
            print("Make sure you're running from the correct directory.", file=sys.stderr)
            
        except Exception as e:
            print(f"Error loading picture: {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

    def update_bitmap(self, picture):
        try:
            wx_image = picture.getWxImage()
            
            bitmap = wx.Bitmap(wx_image)

            self.sizer.Clear(True)
            if self.imageCtrl:
                self.imageCtrl.Destroy()
                self.imageCtrl = None
            if self.placeholder:
                self.placeholder.Destroy()
                self.placeholder = None

            self.imageCtrl = wx.StaticBitmap(self.panel, bitmap=bitmap)
            
            title = picture.getTitle() if hasattr(picture, 'getTitle') else "Image Viewer"
            self.SetTitle(title)

            self.sizer.Add(self.imageCtrl, 0, wx.ALIGN_CENTER, 0)
            self.panel.Layout()
            
            image_size = bitmap.GetSize()
            
            self.SetClientSize(image_size)
            
            self.Center()
            
        except Exception as e:
            print(f"Error updating bitmap: {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)


class ImageViewerApp(wx.App):
    """Custom App class to handle cleanup on exit"""
    
    def OnExit(self):
        """Called when the application is about to exit"""
        print("Application exiting...", file=sys.stderr)
        return super().OnExit()


def main():
    modules_found = []
    for module_name in ['mediaComp', 'mediaComp.core', 'mediaComp.models']:
        if module_name in sys.modules:
            modules_found.append(module_name)
    
    if not modules_found:
        print("Warning: No package modules found in sys.modules", file=sys.stderr)
    
    try:
        if 'makePicture' not in globals():
            print("Warning: makePicture function not found", file=sys.stderr)
    except:
        print("Warning: Cannot check for makePicture function", file=sys.stderr)
    
    # Use custom app class
    app = ImageViewerApp(False)
    
    try:
        window = MainWindow(parent=None)
        app.MainLoop()
    except Exception as e:
        print(f"Application error: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
    finally:
        print("Application finished", file=sys.stderr)

if __name__ == '__main__':
    main()