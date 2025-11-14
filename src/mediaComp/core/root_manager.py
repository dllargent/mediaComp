import tkinter as tk

_root = None
_mainloop_started = False

def get_root():
    global _root
    if _root is None:
        _root = tk.Tk()
        _root.withdraw()
    return _root


def start_mainloop():
    global _mainloop_started
    root = get_root()
    if not _mainloop_started:
        _mainloop_started = True
        root.mainloop()

def _cleanup_if_last_window():
    global _root
    if _root and _root.winfo_exists() and not _root.winfo_children():
        _root.destroy()
        _root = None