import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox
from ..models.Config import ConfigManager

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
    

def requestNumber(message) -> int:
    result = {"value": None}

    def submit():
        try:
            result["value"] = int(entry.get())
            root.destroy()
        except ValueError:
            error_label.config(text="Please enter a valid number")

    def on_close():
        result["value"] = None
        root.destroy()

    root = tk.Tk()
    root.title("Enter a Number")
    root.resizable(False, False)
    _center_window(root, 250, 120)
    _bring_to_front(root)
    root.protocol("WM_DELETE_WINDOW", on_close)

    tk.Label(root, text=message).pack(pady=(10, 5))
    entry = tk.Entry(root, width=30)
    entry.pack(pady=5)
    entry.focus_set()

    entry.bind("<Return>", lambda event: submit())

    tk.Button(root, text="Submit", command=submit).pack(pady=5)
    error_label = tk.Label(root, text="", fg="red")
    error_label.pack()

    root.mainloop()
    return result["value"]


def requestInteger(message) -> int:
    result = {"value": None}

    def submit():
        try:
            result["value"] = int(entry.get())
            root.destroy()
        except ValueError:
            error_label.config(text="Please enter a valid integer")

    def on_close():
        result["value"] = None
        root.destroy()

    root = tk.Tk()
    root.title("Enter an Integer")
    root.resizable(False, False)
    _center_window(root, 250, 120)
    _bring_to_front(root)
    root.protocol("WM_DELETE_WINDOW", on_close)


    tk.Label(root, text=message).pack(pady=(10, 5))
    entry = tk.Entry(root, width=30)
    entry.pack(pady=5)
    entry.focus_set()
    entry.bind("<Return>", lambda event: submit())

    tk.Button(root, text="Submit", command=submit).pack(pady=5)
    error_label = tk.Label(root, text="", fg="red")
    error_label.pack()

    root.mainloop()
    return result["value"]


def requestIntegerInRange(message, min_val, max_val) -> int:
    if min_val >= max_val:
        raise ValueError("min_val >= max_val not allowed")

    result = {"value": None}

    def submit():
        try:
            value = int(entry.get())
            if min_val <= value <= max_val:
                result["value"] = value
                root.destroy()
            else:
                error_label.config(text=f"Enter a number between {min_val} and {max_val}")
        except ValueError:
            error_label.config(text="Please enter a valid integer")

    def on_close():
        result["value"] = None
        root.destroy()

    root = tk.Tk()
    root.title("Enter an Integer in Range")
    root.resizable(False, False)
    _center_window(root, 300, 150)
    _bring_to_front(root)
    root.protocol("WM_DELETE_WINDOW", on_close)

    tk.Label(root, text=f"{message} ({min_val}-{max_val})").pack(pady=(10, 5))
    entry = tk.Entry(root, width=20)
    entry.pack(pady=5)
    entry.focus_set()

    entry.bind("<Return>", lambda event: submit())

    tk.Button(root, text="Submit", command=submit).pack(pady=5)
    error_label = tk.Label(root, text="", fg="red")
    error_label.pack()

    root.mainloop()
    return result["value"]


def requestString(message) -> str:
    result = {"value": None}

    def submit():
        result["value"] = entry.get()
        root.destroy()

    def on_close():
        result["value"] = None
        root.destroy()

    root = tk.Tk()
    root.title("Enter a String")
    root.resizable(False, False)
    _center_window(root, 250, 100)
    _bring_to_front(root)
    root.protocol("WM_DELETE_WINDOW", on_close)

    tk.Label(root, text=message).pack(pady=10)
    entry = tk.Entry(root, width=30)
    entry.pack(pady=5)
    entry.focus_set()

    entry.bind("<Return>", lambda event: submit())

    tk.Button(root, text="Submit", command=submit).pack(pady=5)

    root.mainloop()
    return result["value"]


def showWarning(message) -> None:
    #messagebox.showwarning("Warning", message)

    def on_close():
        root.destroy()

    root = tk.Tk()
    root.title("Warning")
    root.resizable(False, False)
    _center_window(root, 250, 100)
    _bring_to_front(root)
    root.protocol("WM_DELETE_WINDOW", on_close)

    tk.Label(root, text=message).pack(pady=10)

    tk.Button(root, text="Okay", command=on_close).pack(pady=5)

    root.mainloop()

def showInformation(message) -> None:
    messagebox.showinfo("Information", message)



def showError(message) -> None:
    messagebox.showerror("Error", message)