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

def requestNumber(message):
    result = {"value": None}

    def submit():
        result["value"] = entry.get()
        root.destroy()

    root = tk.Tk()
    root.title("Enter a number")
    root.geometry("250x100")

    tk.Label(root, text=message).pack(pady=10)
    entry = tk.Entry(root, width=30)
    entry.pack(pady=5)

    tk.Button(root, text="Submit", command=submit).pack(pady=5)
    root.mainloop()
    return result["value"]


def requestInteger(message):
    result = {"value": None}

    def submit():
        result["value"] = entry.get()
        root.destroy()

    root = tk.Tk()
    root.title("Enter a integer")
    root.geometry("250x100")

    tk.Label(root, text=message).pack(pady=10)
    entry = tk.Entry(root, width=30)
    entry.pack(pady=5)

    tk.Button(root, text="Submit", command=submit).pack(pady=5)
    root.mainloop()
    return result["value"]


def requestIntegerInRange(message, min, max):
    if min >= max:
        raise ValueError("min_val >= max_val not allowed")

    result = {"value": None}

    def submit():
        try:
            value = int(entry.get())
            if min <= value <= max:
                result["value"] = value
                root.quit()
                root.destroy()
            else:
                error_label.config(text=f"Enter a number between {min} and {max}")
        except ValueError:
            error_label.config(text="Please enter a valid integer")

    root = tk.Tk()
    root.title("Enter an Integer")
    root.geometry("300x150")
    root.resizable(False, False)

    tk.Label(root, text = (message + " " + str(min) + "-" + str(max))).pack(pady=(10, 5))
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

    root = tk.Tk()
    root.title("Enter a string")
    root.geometry("250x100")

    tk.Label(root, text=message).pack(pady=10)
    entry = tk.Entry(root, width=30)
    entry.pack(pady=5)

    tk.Button(root, text="Submit", command=submit).pack(pady=5)
    root.mainloop()
    return result["value"]

def showWarning(message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showwarning("Warning",message)


def showInformation(message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Information",message)


def showError(message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error",message)