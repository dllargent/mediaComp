import pytest
from mediaComp import *
 
def get_test_pixel():
    pic = makeEmptyPicture(1, 1)
    return getPixel(pic, 0, 0)


@pytest.mark.parametrize("value", [
    0,           
    128,         
    255,         
])
def test_setRed_getRed(value):
    pixel = get_test_pixel()
    setRed(pixel, value)
    assert getRed(pixel) == value




@pytest.mark.parametrize("value", [
    0,
    128,
    255,
])
def test_setGreen_getGreen(value):
    pixel = get_test_pixel()
    setGreen(pixel, value)
    assert getGreen(pixel) == value



@pytest.mark.parametrize("value", [
    0,
    128,
    255,
])
def test_setBlue_getBlue(value):
    pixel = get_test_pixel()
    setBlue(pixel, value)
    assert getBlue(pixel) == value



@pytest.mark.parametrize("r,g,b", [
    (125, 125, 125),   
    (0,   0,   0),     
    (255, 255, 255),  
    (255, 0,   0),     
    (0,   255, 0),    
    (0,   0,   255),   
    (10,  200, 50),    
])
def test_set_all_channels_independent(r, g, b):
    pixel = get_test_pixel()
    setRed(pixel, r)
    setGreen(pixel, g)
    setBlue(pixel, b)
    assert getRed(pixel)   == r
    assert getGreen(pixel) == g
    assert getBlue(pixel)  == b




@pytest.mark.parametrize("r,g,b", [
    (125, 125, 125),
    (0,   0,   0),
    (255, 255, 255),
    (255, 0,   100),
])
def test_setColor_getColor(r, g, b):
    pixel = get_test_pixel()
    color = makeColor(r, g, b)
    setColor(pixel, color)

    result = getColor(pixel)
    assert getRed(result)   == r
    assert getGreen(result) == g
    assert getBlue(result)  == b


 
def test_setColor_then_getChannels():
    pixel = get_test_pixel()
    color = makeColor(10, 20, 30)
    setColor(pixel, color)

    assert getRed(pixel)   == 10
    assert getGreen(pixel) == 20
    assert getBlue(pixel)  == 30
