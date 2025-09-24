from ..models.Picture import Picture
from ..models.PixelColor import Pixel, Color
import os, random

black = Color(0, 0, 0)
white = Color(255, 255, 255)

def randomPixels(somePic, number) -> None:
    pixelList = []
    pixels = getPixels(somePic)
    for count in range(number):
        pixelList.append(random.choice(pixels))
    if(isinstance(pixelsToPicture(pixelList), Picture)):
        pictureTool(pixelsToPicture(pixelList))

def pictureTool(picture) -> None:
    if isinstance(picture, Picture):
        picture.pictureTool()
    else: 
        print("openPicture(picture): Input is not a picture.")
        raise ValueError

def pixelsToPicture(pixels, defaultColor=white, maxX=100, maxY=100) -> Picture:
    maxX = max([getX(p) for p in pixels])
    maxY = max([getY(p) for p in pixels])
    newpic = makeEmptyPicture(maxX + 1, maxY + 1, defaultColor)
    for pixel in pixels:
        x = getX(pixel)
        y = getY(pixel)
        setColor(getPixelAt(newpic, x, y), getColor(pixel))
    return newpic


def makePicture(filename, defaultColor=white) -> Picture:
    global mediaFolder
    if not isinstance(filename, str):
        return pixelsToPicture(filename, defaultColor=defaultColor)
    if not os.path.isabs(filename):
        filename = mediaFolder + filename
    if not os.path.isfile(filename):
        print("makePicture(filename): There is no file at " + filename)
        raise ValueError
    picture = Picture()
    picture.loadOrFail(filename)
    return picture


def makeEmptyPicture(width, height, acolor=white) -> list:
    if width > 10000 or height > 10000:
        print("makeEmptyPicture(width, height[, acolor]): height and width must be less than 10000 each")
        raise ValueError
    if width <= 0 or height <= 0:
        print("makeEmptyPicture(width, height[, acolor]): height and width must be greater than 0 each")
        raise ValueError
    picture = Picture(width, height, acolor)
    return picture

def getPixels(picture) -> list:
    if not isinstance(picture, Picture):
        print("getPixels(picture): Input is not a picture")
        raise ValueError
    return picture.getPixels()


def getWidth(picture) -> int:
    if not isinstance(picture, Picture):
        print("getWidth(picture): Input is not a picture")
        raise ValueError
    return picture.getWidth()


def getHeight(picture) -> int:
    if not isinstance(picture, Picture):
        print("getHeight(picture): Input is not a picture")
        raise ValueError
    return picture.getHeight()

def show(picture) -> None:
    if not isinstance(picture, Picture):
        print("show(picture): Input is not a picture")
        raise ValueError
    picture.show()

def repaint(picture) -> None:
    if not isinstance(picture, Picture):
        print("repaint(picture): Input is not a picture")
        raise ValueError
    picture.repaint()

def addLine(picture, x1, y1, x2, y2, acolor=black) -> None:
    if not isinstance(picture, Picture):
        print("addLine(picture, x1, y1, x2, y2[, color]): First input is not a picture")
        raise ValueError
    if not isinstance(acolor, Color):
        print("addLine(picture, x1, y1, x2, y2[, color]): Last input is not a color")
        raise ValueError
    picture.addLine(acolor, x1, y1, x2, y2)


def addText(picture, x, y, string, acolor=black) -> None:
    if not isinstance(picture, Picture):
        print("addText(picture, x, y, string[, color]): First input is not a picture")
        raise ValueError
    if not isinstance(acolor, Color):
        print("addText(picture, x, y, string[, color]): Last input is not a color")
        raise ValueError
    
    picture.addText(acolor, x, y, string)


def addRect(picture, x, y, w, h, acolor=black) -> None:
    if not isinstance(picture, Picture):
        print("addRect(picture, x, y, w, h[, color]): First input is not a picture")
        raise ValueError
    if not isinstance(acolor, Color):
        print("addRect(picture, x, y, w, h[, color]): Last input is not a color")
        raise ValueError
    picture.addRect(acolor, x, y, w, h)


def addRectFilled(picture, x, y, w, h, acolor=black) -> None:
    if not isinstance(picture, Picture):
        print("addRectFilled(picture, x, y, w, h[, color]): First input is not a picture")
        raise ValueError
    if not isinstance(acolor, Color):
        print("addRectFilled(picture, x, y, w, h[, color]): Last input is not a color")
        raise ValueError
    picture.addRectFilled(acolor, x, y, w, h)


def addOval(picture, x, y, w, h, acolor=black) -> None:
    if not isinstance(picture, Picture):
        print("addOval(picture, x, y, w, h[, color]): First input is not a picture")
        raise ValueError
    if not isinstance(acolor, Color):
        print("addOval(picture, x, y, w, h[, color]): Last input is not a color")
        raise ValueError
    picture.addOval(acolor, x, y, w, h)


def addOvalFilled(picture, x, y, w, h, acolor=black) -> None:
    if not isinstance(picture, Picture):
        print("addOvalFilled(picture, x, y, w, h[, color]): First input is not a picture")
        raise ValueError
    if not isinstance(acolor, Color):
        print("addOvalFilled(picture, x, y, w, h[, color]): Last input is not a color")
        raise ValueError
    picture.addOvalFilled(acolor, x, y, w, h)


def addArc(picture, x, y, w, h, start, angle, acolor=black) -> None:
    if not isinstance(picture, Picture):
        print("addArc(picture, x, y, w, h, start, angle[, color]): First input is not a picture")
        raise ValueError
    if not isinstance(acolor, Color):
        print("addArc(picture, x, y, w, h, start, angle[, color]): Last input is not a color")
        raise ValueError
    picture.addArc(acolor, x, y, w, h, start, angle)


def addArcFilled(picture, x, y, w, h, start, angle, acolor=black) -> None:
    if not isinstance(picture, Picture):
        print("addArcFilled(picture, x, y, w, h[, color]): First First input is not a picture")
        raise ValueError
    if not isinstance(acolor, Color):
        print("addArcFilled(picture, x, y, w, h, start, angle[, color]): Last input is not a color")
        raise ValueError
    picture.addArcFilled(acolor, x, y, w, h, start, angle)

def getPixelAt(picture, x, y) -> Pixel:
    if not isinstance(picture, Picture):
        print("getPixelAt(picture,x,y): First input is not a picture")
        raise ValueError
    if (x < Picture._PictureIndexOffset) or (x > getWidth(picture) - 1 + Picture._PictureIndexOffset):
        print("getPixelAt(picture,x,y): x (= {}) is less than {} or bigger than the width (= {})".format(x, Picture._PictureIndexOffset, getWidth(picture) - 1 + Picture._PictureIndexOffset))
        raise ValueError
    if (y < Picture._PictureIndexOffset) or (y > getHeight(picture) - 1 + Picture._PictureIndexOffset):
        print("getPixelAt(picture,x,y): y (= {}) is less than {} or bigger than the height (= {})".format(y, Picture._PictureIndexOffset, getHeight(picture) - 1 + Picture._PictureIndexOffset))
        raise ValueError

    return picture.getPixel(x - Picture._PictureIndexOffset, y - Picture._PictureIndexOffset)


def setRed(pixel, value) -> None:
    value = Pixel.correctLevel(value)
    if not isinstance(pixel, Pixel):
        print("setRed(pixel,value): Input is not a pixel")
        raise ValueError
    pixel.setRed(value)


def getRed(pixel) -> int:
    if not isinstance(pixel, Pixel):
        print("getRed(pixel): Input is not a pixel")
        raise ValueError
    return pixel.getRed()


def setBlue(pixel, value) -> None:
    value = Pixel.correctLevel(value)
    if not isinstance(pixel, Pixel):
        print("setBlue(pixel,value): Input is not a pixel")
        raise ValueError
    pixel.setBlue(value)


def getBlue(pixel) -> int:
    if not isinstance(pixel, Pixel):
        print("getBlue(pixel): Input is not a pixel")
        raise ValueError
    return pixel.getBlue()


def setGreen(pixel, value) -> None:
    value = Pixel.correctLevel(value)
    if not isinstance(pixel, Pixel):
        print("setGreen(pixel,value): Input is not a pixel")
        raise ValueError
    pixel.setGreen(value)


def getGreen(pixel) -> int:
    if not isinstance(pixel, Pixel):
        print("getGreen(pixel): Input is not a pixel")
        raise ValueError
    return pixel.getGreen()


def getColor(pixel) -> Color:
    if not isinstance(pixel, Pixel):
        print("getColor(pixel): Input is not a pixel")
        raise ValueError
    return Color(pixel.getColor())


def setColor(pixel, color) -> None:
    if not isinstance(pixel, Pixel):
        print("setColor(pixel,color): First input is not a pixel")
        raise ValueError
    if not isinstance(color, Color):
        print("setColor(pixel,color): Second input is not a color")
        raise ValueError
    pixel.setColor(color)

def getX(pixel) -> int:
    if not isinstance(pixel, Pixel):
        print("getX(pixel): Input is not a pixel")
        raise ValueError
    return pixel.getX() + Picture._PictureIndexOffset


def getY(pixel) -> int:
    if not isinstance(pixel, Pixel):
        print("getY(pixel): Input is not a pixel")
        raise ValueError
    return pixel.getY() + Picture._PictureIndexOffset

def writePictureTo(picture, filename) -> None:
    global mediaFolder
    if not os.path.isabs(filename):
        filename = mediaFolder + filename
    if not isinstance(picture, Picture):
        print("writePictureTo(picture,filename): First input is not a picture")
        raise ValueError
    picture.writeOrFail(filename)

def setAllPixelsToAColor(picture, color) -> None:
    if not isinstance(picture, Picture):
        print("setAllPixelsToAColor(picture,color): First input is not a picture")
        raise ValueError
    if not isinstance(color, Color):
        print("setAllPixelsToAColor(picture,color): Second input is not a color")
        raise ValueError
    picture.setAllPixelsToAColor(color)

def copyInto(origPict, destPict, upperLeftX, upperLeftY) -> Picture:
 if not isinstance(origPict, Picture):
   print("copyInto(origPict, destPict, upperLeftX, upperLeftY): First parameter is not a picture")
   raise ValueError
 if not isinstance(destPict, Picture):
   print("copyInto(origPict, destPict, upperLeftX, upperLeftY): Second parameter is not a picture")
   raise ValueError
 if upperLeftX < 0 or upperLeftX > getWidth(destPict):
   print("copyInto(origPict, destPict, upperLeftX, upperLeftY): upperLeftX must be within the destPict")
   raise ValueError
 if upperLeftY < 0 or upperLeftY > getHeight(destPict):
   print("copyInto(origPict, destPict, upperLeftX, upperLeftY): upperLeftY must be within the destPict")
   raise ValueError
 return origPict.copyInto(destPict, upperLeftX-1, upperLeftY-1)


def duplicatePicture(picture) -> Picture:
    """returns a copy of the picture"""
    if not isinstance(picture, Picture):
        print("duplicatePicture(picture): Input is not a picture")
        raise ValueError
    return Picture(picture)

def cropPicture(picture, upperLeftX, upperLeftY, width, height) -> Picture:
 if not isinstance(picture, Picture):
   print("crop(picture, upperLeftX, upperLeftY, width, height): First parameter is not a picture")
   raise ValueError
 if upperLeftX < 1 or upperLeftX > getWidth(picture):
   print("crop(picture, upperLeftX, upperLeftY, width, height): upperLeftX must be within the picture")
   raise ValueError
 if upperLeftY < 1 or upperLeftY > getHeight(picture):
   print("crop(picture, upperLeftX, upperLeftY, width, height): upperLeftY must be within the picture")
   raise ValueError
 return picture.crop(upperLeftX-1, upperLeftY-1, width, height)

