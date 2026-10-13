import pytest
from mediaComp import *

def test_add_arc_changes_pixel():
    pic = makeEmptyPicture(200, 200)
    black = makeColor(0, 0, 0)
    addArc(pic, 50, 50, 100, 100, 0, 90, black)
    pixels = getPixels(pic)
    changed = any(getRed(p) != 255 or getGreen(p) != 255 or getBlue(p) != 255 for p in pixels)
    assert changed

def test_add_arc_default_color_is_black():
    pic = makeEmptyPicture(200, 200)
    addArc(pic, 50, 50, 100, 100, 0, 360)
    pixels = getPixels(pic)
    has_black = any(getRed(p) == 0 and getGreen(p) == 0 and getBlue(p) == 0 for p in pixels)
    assert has_black

def test_add_arc_custom_color():
    pic = makeEmptyPicture(200, 200)
    red = makeColor(255, 0, 0)
    addArc(pic, 50, 50, 100, 100, 0, 360, red)
    pixels = getPixels(pic)
    has_red = any(getRed(p) == 255 and getGreen(p) == 0 and getBlue(p) == 0 for p in pixels)
    assert has_red

def test_add_arc_does_not_fill_interior():
    pic = makeEmptyPicture(200, 200)
    black = makeColor(0, 0, 0)
    addArc(pic, 50, 50, 100, 100, 0, 360, black)
    center_pixel = getPixelAt(pic, 100, 100)
    assert getRed(center_pixel)   == 255
    assert getGreen(center_pixel) == 255
    assert getBlue(center_pixel)  == 255

def test_add_arc_full_circle():
    pic = makeEmptyPicture(200, 200)
    black = makeColor(0, 0, 0)
    addArc(pic, 50, 50, 100, 100, 0, 360, black)
    pixels = getPixels(pic)
    changed = any(getRed(p) != 255 for p in pixels)
    assert changed

def test_add_arc_partial_angle():
    pic = makeEmptyPicture(200, 200)
    black = makeColor(0, 0, 0)
    addArc(pic, 50, 50, 100, 100, 0, 90, black)
    pixels = getPixels(pic)
    changed = any(getRed(p) != 255 for p in pixels)
    assert changed



def test_add_arc_filled_changes_pixel():
    pic = makeEmptyPicture(200, 200)
    black = makeColor(0, 0, 0)
    addArcFilled(pic, 50, 50, 100, 100, 0, 90, black)
    pixels = getPixels(pic)
    changed = any(getRed(p) != 255 or getGreen(p) != 255 or getBlue(p) != 255 for p in pixels)
    assert changed

def test_add_arc_filled_default_color_is_black():
    pic = makeEmptyPicture(200, 200)
    addArcFilled(pic, 50, 50, 100, 100, 0, 360)
    pixels = getPixels(pic)
    has_black = any(getRed(p) == 0 and getGreen(p) == 0 and getBlue(p) == 0 for p in pixels)
    assert has_black

def test_add_arc_filled_custom_color():
    pic = makeEmptyPicture(200, 200)
    blue = makeColor(0, 0, 255)
    addArcFilled(pic, 50, 50, 100, 100, 0, 360, blue)
    pixels = getPixels(pic)
    has_blue = any(getRed(p) == 0 and getGreen(p) == 0 and getBlue(p) == 255 for p in pixels)
    assert has_blue

def test_add_arc_filled_full_circle():
    pic = makeEmptyPicture(200, 200)
    black = makeColor(0, 0, 0)
    addArcFilled(pic, 50, 50, 100, 100, 0, 360, black)
    pixels = getPixels(pic)
    changed = any(getRed(p) != 255 for p in pixels)
    assert changed

def test_filled_has_more_colored_pixels_than_arc():
    pic_arc = makeEmptyPicture(200, 200)
    pic_filled = makeEmptyPicture(200, 200)
    black = makeColor(0, 0, 0)
    addArc(pic_arc, 50, 50, 100, 100, 0, 360, black)
    addArcFilled(pic_filled, 50, 50, 100, 100, 0, 360, black)
    count_arc = sum(1 for p in getPixels(pic_arc)    if getRed(p) != 255)
    count_filled = sum(1 for p in getPixels(pic_filled) if getRed(p) != 255)
    assert count_filled > count_arc

def test_arc_center_white_filled_center_black():
    pic_arc = makeEmptyPicture(200, 200)
    pic_filled = makeEmptyPicture(200, 200)
    black = makeColor(0, 0, 0)
    addArc(pic_arc, 50, 50, 100, 100, 0, 360, black)
    addArcFilled(pic_filled, 50, 50, 100, 100, 0, 360, black)
    center_arc = getPixelAt(pic_arc, 100, 100)
    center_filled = getPixelAt(pic_filled, 100, 100)
    assert getRed(center_arc)   == 255
    assert getRed(center_filled) == 0
