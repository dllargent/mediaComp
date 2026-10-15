import pytest
from mediaComp import *

def test_add_rect_border_pixel_changed():
    pic = makeEmptyPicture(100, 100)
    black = makeColor(0, 0, 0)
    addRect(pic, 10, 10, 60, 60, black)
    pixel = getPixelAt(pic, 10, 15) 
    assert getRed(pixel) != 255 or getGreen(pixel) != 255 or getBlue(pixel) != 255

def test_add_rect_interior_not_filled():
    pic = makeEmptyPicture(100, 100)
    black = makeColor(0, 0, 0)
    addRect(pic, 10, 10, 60, 60, black)
    pixel = getPixelAt(pic, 40, 40)
    assert getRed(pixel) == 255
    assert getGreen(pixel) == 255
    assert getBlue(pixel)  == 255

def test_add_rect_top_edge():
    pic = makeEmptyPicture(100, 100)
    black = makeColor(0, 0, 0)
    addRect(pic, 10, 10, 60, 60, black)
    pixel = getPixelAt(pic, 10, 15)
    assert getRed(pixel) == 0

def test_add_rect_bottom_edge():
    pic = makeEmptyPicture(100, 100)
    black = makeColor(0, 0, 0)
    addRect(pic, 10, 10, 60, 60, black)
    pixel = getPixelAt(pic, 70, 70)
    assert getRed(pixel) == 0

def test_add_rect_left_edge():
    pic = makeEmptyPicture(100, 100)
    black = makeColor(0, 0, 0)
    addRect(pic, 10, 10, 60, 60, black)
    pixel = getPixelAt(pic, 15, 10)
    assert getRed(pixel) == 0

def test_add_rect_right_edge():
    pic = makeEmptyPicture(100, 100)
    black = makeColor(0, 0, 0)
    addRect(pic, 10, 10, 60, 60, black)
    pixel = getPixelAt(pic, 70, 70)
    assert getRed(pixel) == 0

def test_add_rect_custom_color():
    pic = makeEmptyPicture(100, 100)
    red = makeColor(255, 0, 0)
    addRect(pic, 10, 10, 60, 60, red)
    pixel = getPixelAt(pic, 10, 15)
    assert getRed(pixel) == 255
    assert getGreen(pixel) == 0
    assert getBlue(pixel)  == 0

def test_add_rect_default_color_is_black():
    pic = makeEmptyPicture(100, 100)
    addRect(pic, 10, 10, 60, 60)
    pixel = getPixelAt(pic, 10, 15)
    assert getRed(pixel) == 0
    assert getGreen(pixel) == 0
    assert getBlue(pixel)  == 0

def test_add_rect_does_not_affect_outside_pixels():
    pic = makeEmptyPicture(100, 100)
    black = makeColor(0, 0, 0)
    addRect(pic, 10, 10, 60, 60, black)
    pixel = getPixelAt(pic, 90, 90)
    assert getRed(pixel) == 255
    assert getGreen(pixel) == 255
    assert getBlue(pixel)  == 255

def test_add_rect_blue_border():
    pic = makeEmptyPicture(100, 100)
    blue = makeColor(0, 0, 255)
    addRect(pic, 10, 10, 60, 60, blue)
    pixel = getPixelAt(pic, 10, 15)
    assert getRed(pixel) == 0
    assert getGreen(pixel) == 0
    assert getBlue(pixel)  == 255
 
 
 
 
def test_add_rect_filled_interior_is_filled():
    pic = makeEmptyPicture(100, 100)
    black = makeColor(0, 0, 0)
    addRectFilled(pic, 10, 10, 60, 60, black)
    pixel = getPixelAt(pic, 40, 40)
    assert getRed(pixel)   == 0
    assert getGreen(pixel) == 0
    assert getBlue(pixel)  == 0

def test_add_rect_filled_border_pixel_changed():
    pic = makeEmptyPicture(100, 100)
    black = makeColor(0, 0, 0)
    addRectFilled(pic, 10, 10, 60, 60, black)
    pixel = getPixelAt(pic, 10, 15)
    assert getRed(pixel) != 255 or getGreen(pixel) != 255 or getBlue(pixel) != 255

def test_add_rect_filled_does_not_affect_outside():
    pic = makeEmptyPicture(100, 100)
    black = makeColor(0, 0, 0)
    addRectFilled(pic, 10, 10, 60, 60, black)
    pixel = getPixelAt(pic, 90, 90)
    assert getRed(pixel) == 255
    assert getGreen(pixel) == 255
    assert getBlue(pixel)  == 255

def test_add_rect_filled_custom_color():
    pic = makeEmptyPicture(100, 100)
    red = makeColor(255, 0, 0)
    addRectFilled(pic, 10, 10, 60, 60, red)
    pixel = getPixelAt(pic, 40, 40)
    assert getRed(pixel) == 255
    assert getGreen(pixel) == 0
    assert getBlue(pixel)  == 0

def test_add_rect_filled_default_color_is_black():
    pic = makeEmptyPicture(100, 100)
    addRectFilled(pic, 10, 10, 60, 60)
    pixel = getPixelAt(pic, 40, 40)
    assert getRed(pixel) == 0
    assert getGreen(pixel) == 0
    assert getBlue(pixel)  == 0

def test_add_rect_filled_top_left_corner():
    pic = makeEmptyPicture(100, 100)
    black = makeColor(0, 0, 0)
    addRectFilled(pic, 10, 10, 60, 60, black)
    pixel = getPixelAt(pic, 15, 15)
    assert getRed(pixel) == 0

def test_add_rect_filled_bottom_right_corner():
    pic = makeEmptyPicture(100, 100)
    black = makeColor(0, 0, 0)
    addRectFilled(pic, 10, 10, 60, 60, black)
    pixel = getPixelAt(pic, 70, 70)
    assert getRed(pixel) == 0

def test_add_rect_filled_blue_color():
    pic = makeEmptyPicture(100, 100)
    blue = makeColor(0, 0, 255)
    addRectFilled(pic, 10, 10, 60, 60, blue)
    pixel = getPixelAt(pic, 40, 40)
    assert getRed(pixel) == 0
    assert getGreen(pixel) == 0
    assert getBlue(pixel)  == 255

def test_add_rect_filled_multiple_rects_independent():
    pic = makeEmptyPicture(200, 200)
    red = makeColor(255, 0, 0)
    blue = makeColor(0, 0, 255)
    addRectFilled(pic, 10,  10,  60, 60, red)
    addRectFilled(pic, 100, 100, 60, 60, blue)
    pixel_red = getPixelAt(pic, 40,  40)
    pixel_blue = getPixelAt(pic, 130, 130)
    assert getRed(pixel_red) == 255
    assert getBlue(pixel_blue) == 255
    
    

def test_add_rect_vs_rect_filled_interior_difference():
    pic_hollow = makeEmptyPicture(100, 100)
    pic_filled = makeEmptyPicture(100, 100)
    black = makeColor(0, 0, 0)
    addRect(pic_hollow, 10, 10, 60, 60, black)
    addRectFilled(pic_filled, 10, 10, 60, 60, black)
    pixel_hollow = getPixelAt(pic_hollow, 40, 40)
    pixel_filled = getPixelAt(pic_filled, 40, 40)
    assert getRed(pixel_hollow) == 255
    assert getGreen(pixel_hollow) == 255
    assert getBlue(pixel_hollow) == 255
    assert getRed(pixel_filled) == 0
    assert getGreen(pixel_filled) == 0
    assert getBlue(pixel_filled)  == 0
