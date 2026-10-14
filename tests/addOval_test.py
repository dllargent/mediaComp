import pytest
from mediaComp import*

def test_add_arc_changes_pixel():
    pic = makeEmptyPicture(200, 200)
    black = makeColor(0, 0, 0)
    addArc(pic, 50, 50, 100, 100, 0, 90, black)
    pixels = getPixels(pic)
    assert any(getRed(p) != 255 or getGreen(p) != 255 or getBlue(p) != 255 for p in pixels)

def test_add_arc_custom_color_red():
    pic = makeEmptyPicture(200, 200)
    red = makeColor(255, 0, 0)
    addArc(pic, 50, 50, 100, 100, 0, 90, red)
    pixels = getPixels(pic)
    assert any(getRed(p) != 255 or getGreen(p) != 255 or getBlue(p) != 255 for p in pixels)

def test_add_arc_partial_angle():
    pic = makeEmptyPicture(200, 200)
    black = makeColor(0, 0, 0)
    addArc(pic, 50, 50, 100, 100, 0, 90, black)
    pixels = getPixels(pic)
    assert any(getRed(p) != 255 or getGreen(p) != 255 or getBlue(p) != 255 for p in pixels)

def test_add_arc_180_angle():
    pic = makeEmptyPicture(200, 200)
    black = makeColor(0, 0, 0)
    addArc(pic, 50, 50, 100, 100, 0, 180, black)
    pixels = getPixels(pic)
    assert any(getRed(p) != 255 or getGreen(p) != 255 or getBlue(p) != 255 for p in pixels)

def test_add_arc_does_not_fill_interior():
    pic = makeEmptyPicture(200, 200)
    black = makeColor(0, 0, 0)
    addArc(pic, 50, 50, 100, 100, 0, 90, black)
    center_pixel = getPixelAt(pic, 100, 100)
    assert getRed(center_pixel) == 255 and getGreen(center_pixel) == 255 and getBlue(center_pixel) == 255

def test_add_arc_different_colors_both_change():
    pic1 = makeEmptyPicture(200, 200)
    pic2 = makeEmptyPicture(200, 200)
    addArc(pic1, 50, 50, 100, 100, 0, 90, makeColor(255, 0, 0))
    addArc(pic2, 50, 50, 100, 100, 0, 90, makeColor(0, 0, 255))
    assert any(getRed(p) != 255 or getGreen(p) != 255 or getBlue(p) != 255 for p in getPixels(pic1))
    assert any(getRed(p) != 255 or getGreen(p) != 255 or getBlue(p) != 255 for p in getPixels(pic2))


def test_add_arc_filled_changes_pixel():
    pic = makeEmptyPicture(200, 200)
    black = makeColor(0, 0, 0)
    addArcFilled(pic, 50, 50, 100, 100, 0, 90, black)
    pixels = getPixels(pic)
    assert any(getRed(p) != 255 or getGreen(p) != 255 or getBlue(p) != 255 for p in pixels)

def test_add_arc_filled_custom_color_blue():
    pic = makeEmptyPicture(200, 200)
    blue = makeColor(0, 0, 255)
    addArcFilled(pic, 50, 50, 100, 100, 0, 90, blue)
    pixels = getPixels(pic)
    assert any(getRed(p) != 255 or getGreen(p) != 255 or getBlue(p) != 255 for p in pixels)

def test_add_arc_filled_180_angle():
    pic = makeEmptyPicture(200, 200)
    black = makeColor(0, 0, 0)
    addArcFilled(pic, 50, 50, 100, 100, 0, 180, black)
    pixels = getPixels(pic)
    assert any(getRed(p) != 255 or getGreen(p) != 255 or getBlue(p) != 255 for p in pixels)



def test_filled_has_more_colored_pixels_than_arc(): 
    pic_arc = makeEmptyPicture(200, 200)
    pic_filled = makeEmptyPicture(200, 200)
    black = makeColor(0, 0, 0)
    addArc(pic_arc, 50, 50, 100, 100, 0, 90, black)
    addArcFilled(pic_filled, 50, 50, 100, 100, 0, 90, black)
    count_arc = sum(1 for p in getPixels(pic_arc)    if getRed(p) != 255 or getGreen(p) != 255 or getBlue(p) != 255)
    count_filled = sum(1 for p in getPixels(pic_filled) if getRed(p) != 255 or getGreen(p) != 255 or getBlue(p) != 255)
    assert count_filled > count_arc

def test_arc_changes_fewer_pixels_than_filled():
    pic_arc = makeEmptyPicture(200, 200)
    pic_filled = makeEmptyPicture(200, 200)
    red = makeColor(255, 0, 0)
    addArc(pic_arc,50, 50, 100, 100, 0, 180, red)
    addArcFilled(pic_filled, 50, 50, 100, 100, 0, 180, red)
    count_arc = sum(1 for p in getPixels(pic_arc)    if getRed(p) != 255 or getGreen(p) != 255 or getBlue(p) != 255)
    count_filled = sum(1 for p in getPixels(pic_filled) if getRed(p) != 255 or getGreen(p) != 255 or getBlue(p) != 255)
    assert count_arc < count_filled
