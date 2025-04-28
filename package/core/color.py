from ..models.PixelColor import Pixel, Color

def setColorWrapAround(setting):
    Pixel.setWrapLevels(bool(setting))

def getColorWrapAround():
    return Pixel.getWrapLevels()

def pickAColor():
    return Color.pickAColor()

def distance(c1, c2):
    if not isinstance(c1, Color):
        print("distance(c1,c2): First input is not a color")
        raise ValueError
    if not isinstance(c2, Color):
        print("distance(c1,c2): Second input is not a color")
        raise ValueError
    return c1.distance(c2)

def makeDarker(color):
    if not isinstance(color, Color):
        print("makeDarker(color): Input is not a color")
        raise ValueError
    return Color(color.makeDarker())


def makeLighter(color):
    if not isinstance(color, Color):
        print("makeLighter(color): Input is not a color")
        raise ValueError
    return Color(color.makeLighter())


def makeColor(red, green=None, blue=None):
    return Color(red, green, blue)

