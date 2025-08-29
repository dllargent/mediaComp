import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
from .core import (
        setColorWrapAround, getColorWrapAround, pickAColor, distance, makeDarker, makeLighter, makeColor,
        setMediaFolder, setTestMediaFolder, getMediaFolder,
        showMediaFolder, getShortPath, setLibFolder, pickAFile, pickAFolder,
        randomPixels, pictureTool, pixelsToPicture, makePicture, makeEmptyPicture, getPixels, getWidth, getHeight, show,
        repaint, addLine, addText, addRect, addRectFilled, addOval, addOvalFilled, addArc, addArcFilled,
        getPixelAt, setRed, setGreen, setBlue, getRed, getGreen, getBlue, getColor, setColor, getX, getY,
        writePictureTo, setAllPixelsToAColor, copyInto, duplicatePicture, cropPicture, calculateNeededFiller,
        requestInteger, requestNumber, requestIntegerInRange, requestString, showWarning, showInformation, showError,
        playMovie, writeQuicktime, writeAVI, makeMovie, makeMovieFromInitialFile, addFrameToMovie, writeFramesToDirectory,
        samplesToSound, makeSound, makeEmptySound, makeEmptySoundBySeconds, duplicateSound, getSamples, soundTool,
        play, blockingPlay, stopPlaying, playAtRate, playAtRateDur, playInRange, blockingPlayInRange, playAtRateInRange,
        blockingPlayAtRateInRange, getSamplingRate, getSampleValueAt, setSampleValueAt, setSampleValue,
        getSampleValue, getSound, getNumSamples, getDuration, writeSoundTo, randomSamples, getIndex,
        playNote, turn, turnRight, turnToFace, turnLeft, forward, backward, moveTo, makeTurtle, penUp,
        penDown, drop, getXPos, getYPos, getHeading, makeWorld, getTurtleList, blue, red,
        green, gray, darkGray, lightGray, yellow, orange, pink, magenta, cyan, white, black
    )

__all__ = [
    "setColorWrapAround", "getColorWrapAround", "pickAColor", "distance", "makeDarker", "makeLighter", "makeColor",
    "setMediaFolder", "setTestMediaFolder", "getMediaFolder", 
    "showMediaFolder", "getShortPath", "setLibFolder", "pickAFile", "pickAFolder",
    "randomPixels", "pictureTool", "pixelsToPicture", "makePicture", "makeEmptyPicture", "getPixels", "getWidth", "getHeight", "show",
    "repaint", "addLine", "addText", "addRect", "addRectFilled", "addOval", "addOvalFilled", "addArc", "addArcFilled", 
    "getPixelAt", "setRed", "setGreen", "setBlue", "getRed", "getGreen", "getBlue", "getColor", "setColor", "getX", "getY", 
    "writePictureTo", "setAllPixelsToAColor", "copyInto", "duplicatePicture", "cropPicture", "calculateNeededFiller",
    "requestInteger", "requestNumber", "requestIntegerInRange", "requestString", "showWarning", "showInformation", "showError",
    "playMovie", "writeQuicktime", "writeAVI", "makeMovie", "makeMovieFromInitialFile", "addFrameToMovie", "writeFramesToDirectory", 
    "samplesToSound", "makeSound", "makeEmptySound", "makeEmptySoundBySeconds", "duplicateSound", "getSamples", "soundTool", 
    "play", "blockingPlay", "stopPlaying", "playAtRate", "playAtRateDur", "playInRange", "blockingPlayInRange", "playAtRateInRange", 
    "blockingPlayAtRateInRange", "getSamplingRate", "getSampleValueAt", "setSampleValueAt", "setSampleValue", 
    "getSampleValue", "getSound", "getNumSamples", "getDuration", "writeSoundTo", "randomSamples", "getIndex", 
    "playNote", "turn", "turnRight", "turnToFace", "turnLeft", "forward", "backward", "moveTo", "makeTurtle", "penUp", 
    "penDown", "drop", "getXPos", "getYPos", "getHeading", "makeWorld", "getTurtleList", "blue", "red", 
    "green", "gray", "darkGray", "lightGray", "yellow", "orange", "pink", "magenta", "cyan", "white", "black", "config"
]

from mediaComp.models.Config import config
