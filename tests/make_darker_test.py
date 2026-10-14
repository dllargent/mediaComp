import math
import pytest
from mediaComp import *


def test_make_darker_reduces_values():
    c = makeColor(100, 100, 100)
    darker = c.makeDarker()
    expected = round(100 * 7.0 / 10.0)
    assert darker.getRed()== expected
    assert darker.getGreen() == expected
    assert darker.getBlue()  == expected

def test_make_darker_known_value():
    c = makeColor(200, 0, 0)
    darker = c.makeDarker()
    assert darker.getRed() == pytest.approx(140, abs=1)
    assert darker.getGreen() == 0
    assert darker.getBlue()  == 0

def test_make_darker_black_stays_black():
    c = makeColor(0, 0, 0)
    darker = c.makeDarker()
    assert darker.getRed() == 0
    assert darker.getGreen() == 0
    assert darker.getBlue()  == 0

def test_make_darker_returns_color_object():
    c = makeColor(100, 150, 200)
    darker = c.makeDarker()
    assert darker is not None
    assert type(darker).__name__ == 'Color'

def test_make_darker_does_not_modify_original():
    c = makeColor(100, 150, 200)
    _ = c.makeDarker()
    assert c.getRed() == 100
    assert c.getGreen() == 150
    assert c.getBlue()  == 200

def test_make_darker_twice():
    c = makeColor(200, 200, 200)
    darker_twice = c.makeDarker().makeDarker()
    expected = round(200 * 0.7 * 0.7)
    assert darker_twice.getRed() == pytest.approx(expected, abs=1)





def test_make_lighter_increases_values():
    c = makeColor(70, 70, 70)
    lighter = c.makeLighter()
    expected = round(70 * 10.0 / 7.0)
    assert lighter.getRed() == pytest.approx(expected, abs=1)
    assert lighter.getGreen() == pytest.approx(expected, abs=1)
    assert lighter.getBlue()== pytest.approx(expected, abs=1)

def test_make_lighter_black_becomes_333():
    c = makeColor(0, 0, 0)
    lighter = c.makeLighter()
    assert lighter.getRed() == 3
    assert lighter.getGreen() == 3
    assert lighter.getBlue()  == 3

def test_make_lighter_returns_color_object():
    c = makeColor(100, 100, 100)
    lighter = c.makeLighter()
    assert lighter is not None
    assert type(lighter).__name__ == 'Color'

def test_make_lighter_does_not_modify_original():
    c = makeColor(100, 150, 200)
    _ = c.makeLighter()
    assert c.getRed() == 100
    assert c.getGreen() == 150
    assert c.getBlue() == 200

def test_make_lighter_clamps_to_255():
    c = makeColor(240, 240, 240)
    lighter = c.makeLighter()
    assert lighter.getRed() <= 255
    assert lighter.getGreen() <= 255
    assert lighter.getBlue() <= 255

def test_make_lighter_and_darker_approximate_inverse():
    c = makeColor(100, 150, 200)
    result = c.makeLighter().makeDarker()
    assert result.getRed()   == pytest.approx(c.getRed(),   abs=25)
    assert result.getGreen() == pytest.approx(c.getGreen(), abs=25)
    assert result.getBlue()  == pytest.approx(c.getBlue(),  abs=25)