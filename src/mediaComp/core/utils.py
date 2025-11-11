import os
import sys
import subprocess
from math import inf
import tkinter as tk
from tkinter import messagebox
from ..models.Config import ConfigManager
from pathlib import Path
from mediaComp import get_root, _cleanup_if_last_window

config = ConfigManager() 

def setMediaFolder(path=None) -> str:
    if path is None:
        pickMediaPath()
    elif os.path.exists(path):
        config.setMediaPath(path)
    else:
        config.setMediaPath("C:\\")
    return config.getMediaPath()

def setTestMediaFolder() -> str:
    config.setMediaPath(os.getcwd() + os.sep)

def getMediaFolder(filename="") -> str:
    return config.getMediaPath(filename)

def showMediaFolder() -> None:
    print("The media path is currently:", config.getMediaPath())

def getShortPath(filename) -> str:
    dirs = filename.split(os.sep)
    if len(dirs) < 1:
        return "."
    elif len(dirs) == 1:
        return str(dirs[0])
    else:
        return os.path.join(dirs[-2], dirs[-1])

def setLibFolder(directory=None) -> str:
    if directory is None:
        directory = pickAFolder()
    if os.path.isdir(directory):
        sys.path.insert(0, directory)
    elif directory:
        raise ValueError("There is no directory at " + directory)
    return directory

def pickAFile() -> str:
    directory = config.getSessionPath()
    scriptpath = os.path.join(config.getMEDIACOMPPath(), 'scripts', 'filePicker.py')
    path = subprocess.check_output([sys.executable, scriptpath, 'file', directory]).decode().strip()
    if path:
        config.setSessionPath(os.path.dirname(path))
        return path
    return None

def pickAFolder() -> str:
    directory = config.getSessionPath()
    scriptpath = os.path.join(config.getMEDIACOMPPath(), 'scripts', 'filePicker.py')
    path = subprocess.check_output([sys.executable, scriptpath, 'folder', directory]).decode().strip()
    if path:
        config.setSessionPath(path)
        return os.path.join(path, '')
    return None

def pickMediaPath() -> None:
    path = pickAFolder()
    if path:
        config.setMediaPath(path)

def calculateNeededFiller(message, width=100) -> str:
    fillerNeeded = width - len(message)
    if fillerNeeded < 0:
        fillerNeeded = 0
    return fillerNeeded * " "

def requestNumber(message) -> int:
    return _requestInfoDialog("Enter a Number", message, "requestNum")

def requestInteger(message) -> int:
    return _requestInfoDialog("Enter an Integer", message, "requestInt")

def requestIntegerInRange(message, min_val, max_val) -> int:
    return _requestInfoDialog("Enter an Integer in Range", message, "requestInt", min_val, max_val)

def requestString(message) -> str:
    return _requestInfoDialog("Enter a String", message, "requestString")


def showWarning(message) -> None:
    _showDialog("Warning", message)

def showInformation(message) -> None:
    _showDialog("Information", message)

def showError(message) -> None:
    _showDialog("Error", message)

def _requestInfoDialog(title, message, typeOfDialog, min_val=-inf, max_val=inf):
    if min_val >= max_val:
        raise ValueError("min_val >= max_val not allowed")
    result = {"value": None}

    def on_close():
        result["value"] = None
        root.destroy()

    root = tk.Tk()
    root.title(title)
    root.resizable(False, False)
    #_center_window(root, 250, 130)
    #_bring_to_front(root)
    root.protocol("WM_DELETE_WINDOW", on_close)

    msg_label = tk.Label(root, text=message, wraplength=300, justify="center")
    msg_label.pack(pady=10)
    def submit():
        if typeOfDialog == "requestInt":
            try:
                value = int(entry.get())
                if min_val <= value <= max_val:
                    result["value"] = value
                    root.destroy()
                else:
                    error_label.config(text=f"Enter a number between {min_val} and {max_val}")
            except ValueError:
                error_label.config(text="Please enter a valid integer")
        elif typeOfDialog == "requestNum":
            try:
                value = float(entry.get())
                result["value"] = value
                root.destroy()
            except ValueError:
                error_label.config(text="Please enter a valid number")
        else:
            result["value"] = entry.get()
            root.destroy()

    entry = tk.Entry(root, width=30)
    entry.pack(pady=5)
    entry.focus_set()

    entry.bind("<Return>", lambda event: submit())
    tk.Button(root, text="OK", command=submit).pack(pady=5)
    error_label = tk.Label(root, text="", fg="red")
    error_label.pack()

    root.update_idletasks()
    _center_window(root, root.winfo_reqwidth(), root.winfo_reqheight())
    _bring_to_front(root)
    root.mainloop()
    return result["value"]

def _showDialog(title, message):
    def on_close():
        root.destroy()

    root = tk.Tk()
    root.title(title)
    root.resizable(False, False)
    root.protocol("WM_DELETE_WINDOW", on_close)

    match title:
        case "Warning":
            icon = Path(__file__).resolve().parent.parent / "assets" / f"warning.png"
        case "Information":
            icon = Path(__file__).resolve().parent.parent / "assets" / f"info.png"
        case "Error":
            icon = Path(__file__).resolve().parent.parent / "assets" / f"error.png"

    img = tk.PhotoImage(file=icon)
    root.iconphoto(True, img)

    tk.Label(root, text=message, wraplength=300, justify="center").pack(pady=10)
    button = tk.Button(root, text="OK", command=on_close)
    button.pack(pady=(0, 15))

    # Let Tk compute how large the window should be
    root.update_idletasks()
    width = root.winfo_reqwidth()
    height = root.winfo_reqheight()

    # Optionally clamp to screen width/height
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    width = min(width, int(screen_w * 0.8))
    height = min(height, int(screen_h * 0.8))

    # Center and bring forward
    _center_window(root, width, height)
    _bring_to_front(root)

    # Bind Enter key and run
    root.bind("<Return>", lambda event: on_close())
    root.mainloop()

def _center_window(root, width, height):
    root.update_idletasks()
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    x = max(0, x)
    y = max(0, y)
    
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.update_idletasks()


def _bring_to_front(root) -> None:
    root.lift()
    root.attributes("-topmost", True)
    root.after_idle(root.attributes, "-topmost", False)
    root.focus_force()
    root.grab_set()
