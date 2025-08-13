import os
import sys
import subprocess
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox

'''
def setMediaPath(file=None):
    global mediaFolder
    if(file == None):
        FileChooser.pickMediaPath()
    elif os.path.exists(file):
        FileChooser.setMediaPath(file)
    else:
        FileChooser.setMediaPath("C:\\")
    mediaFolder = getMediaPath()
    return mediaFolder

def getMediaPath(filename=""):
    return str(FileChooser.getMediaPath(filename))

def setMediaFolder(file=None):
    return setMediaPath(file)

def setTestMediaFolder():
    global mediaFolder
    mediaFolder = os.getcwd() + os.sep

def getMediaFolder(filename=""):
    return str(getMediaPath(filename))

def showMediaFolder():
    global mediaFolder
    print("The media path is currently: ", mediaFolder)

def getShortPath(filename):
    dirs = filename.split(os.sep)
    if len(dirs) < 1:
        return "."
    elif len(dirs) == 1:
        return str(dirs[0])
    else:
        return str(dirs[len(dirs) - 2] + os.sep + dirs[len(dirs) - 1])
    
def setLibPath(directory=None):
    if directory is None:
        directory = pickAFolder()

    if os.path.isdir(directory):
        sys.path.insert(0, directory)
    elif directory is not None:
        raise ValueError("There is no directory at " + directory)

    return directory


def pickAFile():
    return FileChooser.pickAFile()


def pickAFolder():
    dir = FileChooser.pickADirectory()
    if (dir != None):
        return dir
    return None
'''
from ..models.Config import ConfigManager

config = ConfigManager() 

def setMediaFolder(path=None):
    if path is None:
        pickMediaPath()
    elif os.path.exists(path):
        config.setMediaPath(path)
    else:
        config.setMediaPath("C:\\")
    return config.getMediaPath()

def setTestMediaFolder():
    config.setMediaPath(os.getcwd() + os.sep)

def getMediaFolder(filename=""):
    return config.getMediaPath(filename)

def showMediaFolder():
    print("The media path is currently:", config.getMediaPath())

def getShortPath(filename):
    dirs = filename.split(os.sep)
    if len(dirs) < 1:
        return "."
    elif len(dirs) == 1:
        return str(dirs[0])
    else:
        return os.path.join(dirs[-2], dirs[-1])

def setLibFolder(directory=None):
    if directory is None:
        directory = pickAFolder()
    if os.path.isdir(directory):
        sys.path.insert(0, directory)
    elif directory:
        raise ValueError("There is no directory at " + directory)
    return directory

def pickAFile():
    directory = config.getSessionPath()
    scriptpath = os.path.join(config.getMEDIACOMPPath(), 'scripts', 'filePicker.py')
    path = subprocess.check_output([sys.executable, scriptpath, 'file', directory]).decode().strip()
    if path:
        config.setSessionPath(os.path.dirname(path))
        return path
    return None

def pickAFolder():
    directory = config.getSessionPath()
    scriptpath = os.path.join(config.getMEDIACOMPPath(), 'scripts', 'filePicker.py')
    path = subprocess.check_output([sys.executable, scriptpath, 'folder', directory]).decode().strip()
    if path:
        config.setSessionPath(path)
        return os.path.join(path, '')
    return None

def pickMediaPath():
    path = pickAFolder()
    if path:
        config.setMediaPath(path)

def calculateNeededFiller(message, width=100):
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


def _bring_to_front(root):
    root.lift()
    root.attributes("-topmost", True)
    root.after_idle(root.attributes, "-topmost", False)
    

def requestNumber(message):
    result = {"value": None}

    def submit():
        result["value"] = entry.get()
        root.destroy()

    def on_close():
        result["value"] = None
        root.destroy()

    root = tk.Tk()
    root.title("Enter a Number")

    tk.Label(root, text=message).pack(pady=10)
    entry = tk.Entry(root, width=30)
    entry.pack(pady=5)
    entry.focus_set()

    tk.Button(root, text="Submit", command=submit).pack(pady=5)
    _center_window(root, 250, 100)
    root.deiconify()  
    _bring_to_front(root)
    root.protocol("WM_DELETE_WINDOW", on_close)

    root.mainloop()
    return result["value"]


def requestInteger(message):
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
    _center_window(root, 250, 120)
    _bring_to_front(root)
    root.protocol("WM_DELETE_WINDOW", on_close)

    tk.Label(root, text=message).pack(pady=(10, 5))
    entry = tk.Entry(root, width=30)
    entry.pack(pady=5)
    entry.focus_set()

    tk.Button(root, text="Submit", command=submit).pack(pady=5)
    error_label = tk.Label(root, text="", fg="red")
    error_label.pack()

    root.mainloop()
    return result["value"]


def requestIntegerInRange(message, min_val, max_val):
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
    _center_window(root, 300, 150)
    _bring_to_front(root)
    root.protocol("WM_DELETE_WINDOW", on_close)

    tk.Label(root, text=f"{message} ({min_val}-{max_val})").pack(pady=(10, 5))
    entry = tk.Entry(root, width=20)
    entry.pack(pady=5)
    entry.focus_set()

    tk.Button(root, text="Submit", command=submit).pack(pady=5)
    error_label = tk.Label(root, text="", fg="red")
    error_label.pack()

    root.mainloop()
    return result["value"]


def requestString(message):
    result = {"value": None}

    def submit():
        result["value"] = entry.get()
        root.destroy()

    def on_close():
        result["value"] = None
        root.destroy()

    root = tk.Tk()
    root.title("Enter a String")
    _center_window(root, 250, 100)
    _bring_to_front(root)
    root.protocol("WM_DELETE_WINDOW", on_close)

    tk.Label(root, text=message).pack(pady=10)
    entry = tk.Entry(root, width=30)
    entry.pack(pady=5)
    entry.focus_set()

    tk.Button(root, text="Submit", command=submit).pack(pady=5)

    root.mainloop()
    return result["value"]


def showWarning(message):
    root = tk.Tk()
    root.withdraw()
    _bring_to_front(root)
    messagebox.showwarning("Warning", message, parent=root)
    root.destroy()


def showInformation(message):
    root = tk.Tk()
    root.withdraw()
    _bring_to_front(root)
    messagebox.showinfo("Information", message, parent=root)
    root.destroy()


def showError(message):
    root = tk.Tk()
    root.withdraw()
    _bring_to_front(root)
    messagebox.showerror("Error", message, parent=root)
    root.destroy()