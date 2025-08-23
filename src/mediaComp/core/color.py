from ..models.PixelColor import Pixel, Color

black = Color(0, 0, 0)
white = Color(255, 255, 255)
blue = Color(0, 0, 255)
red = Color(255, 0, 0)
green = Color(0, 255, 0)
gray = Color(128, 128, 128)
darkGray = Color(64, 64, 64)
lightGray = Color(192, 192, 192)
yellow = Color(255, 255, 0)
orange = Color(255, 200, 0)
pink = Color(255, 175, 175)
magenta = Color(255, 0, 255)
cyan = Color(0, 255, 255)

def setColorWrapAround(setting)-> None:
    Pixel.setWrapLevels(bool(setting))

def getColorWrapAround() -> bool:
    return Pixel.getWrapLevels()

def pickAColor() -> Color:
    return Color.pickAColor()

def distance(c1, c2) -> float:
    if not isinstance(c1, Color):
        print("distance(c1,c2): First input is not a color")
        raise ValueError
    if not isinstance(c2, Color):
        print("distance(c1,c2): Second input is not a color")
        raise ValueError
    return c1.distance(c2)

def makeDarker(color) -> Color:
    if not isinstance(color, Color):
        print("makeDarker(color): Input is not a color")
        raise ValueError
    return Color(color.makeDarker())

def makeLighter(color) -> Color:
    if not isinstance(color, Color):
        print("makeLighter(color): Input is not a color")
        raise ValueError
    return Color(color.makeLighter())


def makeColor(red, green=None, blue=None) -> Color:
    return Color(red, green, blue)

