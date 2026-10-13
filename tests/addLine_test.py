import pytest
from mediaComp import *

def test_add_line_changes_pixel():
    pic = makeEmptyPicture(100, 100)
    black = makeColor(0, 0, 0)
    addLine(pic, 0, 0, 99, 0, black)
    pixel = getPixelAt(pic, 50, 0)
    assert getRed(pixel) != 255 or getGreen(pixel) != 255 or getBlue(pixel) != 255

def test_add_line_default_color_is_black():
    pic = makeEmptyPicture(100, 100)
    addLine(pic, 0, 50, 99, 50)
    pixel = getPixelAt(pic, 50, 50)
    assert getRed(pixel) == 0
    assert getGreen(pixel) == 0
    assert getBlue(pixel)  == 0

def test_add_line_custom_color():
    pic = makeEmptyPicture(100, 100)
    red = makeColor(255, 0, 0)
    addLine(pic, 0, 10, 99, 10, red)
    pixel = getPixelAt(pic, 50, 10)
    assert getRed(pixel) == 255
    assert getGreen(pixel) == 0
    assert getBlue(pixel)  == 0

def test_add_line_start_pixel_changed():
    pic = makeEmptyPicture(100, 100)
    black = makeColor(0, 0, 0)
    addLine(pic, 10, 10, 90, 10, black)
    pixel = getPixelAt(pic, 10, 10)
    assert getRed(pixel) == 0

def test_add_line_end_pixel_changed():
    pic = makeEmptyPicture(100, 100)
    black = makeColor(0, 0, 0)
    addLine(pic, 10, 10, 90, 10, black)
    pixel = getPixelAt(pic, 90, 10)
    assert getRed(pixel) == 0

def test_add_line_does_not_affect_other_pixels():
    pic = makeEmptyPicture(100, 100)
    black = makeColor(0, 0, 0)
    addLine(pic, 0, 0, 99, 0, black)  
    pixel = getPixelAt(pic, 50, 50)  
    assert getRed(pixel) == 255
    assert getGreen(pixel) == 255
    assert getBlue(pixel)  == 255

def test_add_line_vertical():
    pic = makeEmptyPicture(100, 100)
    black = makeColor(0, 0, 0)
    addLine(pic, 50, 0, 50, 99, black)
    pixel = getPixelAt(pic, 50, 50)
    assert getRed(pixel) == 0

def test_add_line_diagonal():
    pic = makeEmptyPicture(100, 100)
    black = makeColor(0, 0, 0)
    addLine(pic, 0, 0, 99, 99, black)
    pixel = getPixelAt(pic, 0, 0)
    assert getRed(pixel) == 0

def test_add_line_blue_color():
    pic = makeEmptyPicture(100, 100)
    blue = makeColor(0, 0, 255)
    addLine(pic, 0, 20, 99, 20, blue)
    pixel = getPixelAt(pic, 50, 20)
    assert getRed(pixel) == 0
    assert getGreen(pixel) == 0
    assert getBlue(pixel)  == 255

def test_add_line_multiple_lines_independent():
    pic = makeEmptyPicture(100, 100)
    red  = makeColor(255, 0, 0)
    blue = makeColor(0, 0, 255)
    addLine(pic, 0, 10, 99, 10, red)
    addLine(pic, 0, 20, 99, 20, blue)
    pixel_red  = getPixelAt(pic, 50, 10)
    pixel_blue = getPixelAt(pic, 50, 20)
    assert getRed(pixel_red) == 255
    assert getBlue(pixel_blue)  == 255
