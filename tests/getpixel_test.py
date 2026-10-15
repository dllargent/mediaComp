import pytest
import os
from mediaComp import *

def test_get_pixels_returns_list():
    pic = makeEmptyPicture(10, 10)
    pixels = getPixels(pic)
    assert isinstance(pixels, list)

def test_get_pixels_correct_count():
    pic = makeEmptyPicture(10, 20)
    pixels = getPixels(pic)
    assert len(pixels) == 10 * 20

def test_get_pixels_not_empty():
    pic = makeEmptyPicture(5, 5)
    pixels = getPixels(pic)
    assert len(pixels) > 0



def test_get_pixel_at_returns_pixel():
    pic = makeEmptyPicture(10, 10)
    pixel = getPixelAt(pic, 0, 0)
    assert pixel is not None
    assert type(pixel).__name__ == 'Pixel'

def test_get_pixel_at_correct_color():
    blue = makeColor(0, 0, 255)
    pic = makeEmptyPicture(10, 10, blue)
    pixel = getPixelAt(pic, 5, 5)
    assert getRed(pixel) == 0
    assert getGreen(pixel) == 0
    assert getBlue(pixel)== 255

def test_get_pixel_at_corner():
    pic = makeEmptyPicture(10, 10)
    assert getPixelAt(pic, 0, 0) is not None
    assert getPixelAt(pic, 9, 0) is not None
    assert getPixelAt(pic, 0, 9) is not None
    assert getPixelAt(pic, 9, 9) is not None
    
    

def test_get_x_returns_correct_value():
    pic = makeEmptyPicture(10, 10)
    pixel = getPixelAt(pic, 3, 7)
    assert getX(pixel) == 3

def test_get_y_returns_correct_value():
    pic = makeEmptyPicture(10, 10)
    pixel = getPixelAt(pic, 3, 7)
    assert getY(pixel) == 7

def test_get_x_not_equal_to_y():
    pic = makeEmptyPicture(20, 20)
    pixel = getPixelAt(pic, 2, 8)
    assert getX(pixel) != getY(pixel)

def test_get_x_y_from_get_pixels():
    pic = makeEmptyPicture(10, 20)
    pixels = getPixels(pic)
    for pixel in pixels:
        assert 0 <= getX(pixel) < 10
        assert 0 <= getY(pixel) < 20
