import pytest
import os
from mediaComp import *

IMAGE_PATH = os.path.join(os.path.dirname(__file__), 'sources', 'arch.jpg')


def test_get_width_returns_correct_value():
    pic = makeEmptyPicture(100, 200)
    assert getWidth(pic) == 100

def test_get_height_returns_correct_value():
    pic = makeEmptyPicture(100, 200)
    assert getHeight(pic) == 200

def test_get_width_is_positive():
    pic = makeEmptyPicture(50, 50)
    assert getWidth(pic) > 0

def test_get_height_is_positive():
    pic = makeEmptyPicture(50, 50)
    assert getHeight(pic) > 0

def test_get_width_not_equal_to_height():
    pic = makeEmptyPicture(300, 100)
    assert getWidth(pic) != getHeight(pic)

def test_get_width_from_loaded_picture():
    pic = makePicture(IMAGE_PATH)
    assert getWidth(pic) > 0

def test_get_height_from_loaded_picture():
    pic = makePicture(IMAGE_PATH)
    assert getHeight(pic) > 0

def test_get_width_after_duplicate():
    original = makeEmptyPicture(123, 456)
    copy = duplicatePicture(original)
    assert getWidth(copy) == 123

def test_get_height_after_duplicate():
    original = makeEmptyPicture(123, 456)
    copy = duplicatePicture(original)
    assert getHeight(copy) == 456
