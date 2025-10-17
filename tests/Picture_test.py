from mediaComp.models.Picture import Picture
from mediaComp.models.PixelColor import Color



def test_getExtension():
    white = Color(255, 255, 255)
    image = Picture(100, 100, white)
    assert image.getExtension() == ".jpg"
    assert image.getExtension() != ".png"

def test_setAllPixelsToAColor():
    white = Color(255, 255, 255)
    black = Color(0, 0, 0)
    image = Picture(100, 100, white)
    image.setAllPixelsToAColor(black)
    pixel1 = image.getPixel(0, 0)
    pixel2 = image.getPixel(50, 50)
    pixel3 = image.getPixel(99, 99)
    assert pixel1.getColor().getRGB() ==(0,0,0)
    assert pixel2.getColor().getRGB() ==(0,0,0)
    assert pixel3.getColor().getRGB() ==(0,0,0)

