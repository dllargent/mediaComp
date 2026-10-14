import pytest
import os
from mediaComp import *

IMAGE_PATH = os.path.join(os.path.dirname(__file__), 'sources', 'arch.jpg')
 
def test_make_empty_picture_returns_picture():
    pic = makeEmptyPicture(100, 200)
    assert pic is not None
    assert type(pic).__name__== 'Picture'

def test_make_empty_picture_correct_width():
    pic = makeEmptyPicture(100, 200)
    assert getWidth(pic) == 100

def test_make_empty_picture_correct_height():
    pic = makeEmptyPicture(100, 200)
    assert getHeight(pic) == 200

def test_make_empty_picture_default_color_is_white():
    pic = makeEmptyPicture(10, 10)
    pixel = getPixelAt(pic, 0, 0)
    assert getRed(pixel) == 255
    assert getGreen(pixel) == 255
    assert getBlue(pixel) == 255

def test_make_empty_picture_with_color():
    red = makeColor(255, 0, 0)
    pic = makeEmptyPicture(10, 10, red)
    pixel = getPixelAt(pic, 0, 0)
    assert getRed(pixel) == 255
    assert getGreen(pixel) == 0
    assert getBlue(pixel) == 0

def test_make_empty_picture_small_size():
    pic = makeEmptyPicture(1, 1)
    assert getWidth(pic) == 1
    assert getHeight(pic) == 1

 
 
 
def test_make_picture_returns_picture():
    pic = makePicture(IMAGE_PATH)
    assert pic is not None
    assert type(pic).__name__ == 'Picture'

def test_make_picture_has_positive_width():
    pic = makePicture(IMAGE_PATH)
    assert getWidth(pic) > 0

def test_make_picture_has_positive_height():
    pic = makePicture(IMAGE_PATH)
    assert getHeight(pic) > 0




def test_duplicate_picture_returns_picture():
    original = makeEmptyPicture(50, 50)
    copy = duplicatePicture(original)
    assert copy is not None
    assert type(copy).__name__ == 'Picture'

def test_duplicate_picture_same_width():
    original = makeEmptyPicture(80, 60)
    copy = duplicatePicture(original)
    assert getWidth(copy) == getWidth(original)

def test_duplicate_picture_same_height():
    original = makeEmptyPicture(80, 60)
    copy = duplicatePicture(original)
    assert getHeight(copy) == getHeight(original)

def test_duplicate_picture_same_pixel_color():
    red = makeColor(255, 0, 0)
    original = makeEmptyPicture(10, 10, red)
    copy = duplicatePicture(original)
    pixel = getPixelAt(copy, 0, 0)
    assert getRed(pixel) == 255
    assert getGreen(pixel) == 0
    assert getBlue(pixel)  == 0

def test_duplicate_picture_is_independent():
    original = makeEmptyPicture(10, 10)
    copy = duplicatePicture(original)
    pixel = getPixelAt(copy, 0, 0)
    setRed(pixel, 123)
    original_pixel = getPixelAt(original, 0, 0)
    assert getRed(original_pixel) == 255
