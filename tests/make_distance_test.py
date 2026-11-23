import math
import pytest
from mediaComp import *

def test_distance_same_color_is_zero():
    c1 = makeColor(100, 100, 100)
    c2 = makeColor(100, 100, 100)
    assert c1.distance(c2) == 0.0

def test_distance_known_value():
    c1 = makeColor(255, 0, 0)
    c2 = makeColor(0, 0, 0)
    assert c1.distance(c2) == pytest.approx(255.0)

def test_distance_three_channels():
    c1 = makeColor(3, 4, 0)
    c2 = makeColor(0, 0, 0)
    assert c1.distance(c2) == pytest.approx(5.0)

def test_distance_is_symmetric():
    c1 = makeColor(200, 100, 50)
    c2 = makeColor(50,  80, 200)
    assert c1.distance(c2) == pytest.approx(c2.distance(c1))
    
    

def test_distance_invalid_input_returns_none():
    c = makeColor(100, 100, 100)
    result = c.distance("not a color")
    assert result is None
 
