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
    scriptpath = os.path.join(config.getJES4PYPath(), 'package/scripts', 'filePicker.py')
    path = subprocess.check_output([sys.executable, scriptpath, 'file', directory]).decode().strip()
    if path:
        config.setSessionPath(os.path.dirname(path))
        return path
    return None

def pickAFolder():
    directory = config.getSessionPath()
    scriptpath = os.path.join(config.getJES4PYPath(), 'package/scripts', 'filePicker.py')
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
    root = tk.Tk()
    root.withdraw()
    filler = calculateNeededFiller(message, 60)
    userInput = simpledialog.askfloat("Enter a number", message + filler)
    root.destroy()
    return userInput


def requestInteger(message):
    root = tk.Tk()
    root.withdraw()
    filler = calculateNeededFiller(message, 60)
    userInput = simpledialog.askinteger("Enter an integer", message + filler)
    root.destroy()
    return userInput


def requestIntegerInRange(message, min, max):

    if min >= max:
        print("requestIntegerInRange(message, min, max): min >= max not allowed")
        raise ValueError
    root = tk.Tk()
    root.withdraw()
    filler = calculateNeededFiller(message, 80)
    userInput = simpledialog.askinteger("Enter an integer in a range", message + filler, minvalue=min, maxvalue=max)
    root.destroy()
    return userInput


def requestString(message):
    root = tk.Tk()
    root.withdraw()
    filler = calculateNeededFiller(message)
    userInput = simpledialog.askstring("Enter a string", message + filler)
    root.destroy()
    return userInput

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