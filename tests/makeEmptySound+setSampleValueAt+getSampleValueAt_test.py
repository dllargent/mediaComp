import pytest
from mediaComp import *

def test_makeEmptySound_returns_object():
    sound = makeEmptySound(22050)
    assert sound is not None

def test_makeEmptySound_correct_numsamples():
    sound = makeEmptySound(22050)
    assert getNumSamples(sound) == 22050

def test_makeEmptySound_all_zeros_first():
    sound = makeEmptySound(22050)
    assert getSampleValueAt(sound, 0) == 0
    
    

def test_makeEmptySound_all_zeros_middle():
    sound = makeEmptySound(22050)
    assert getSampleValueAt(sound, 11025) == 0

def test_makeEmptySound_all_zeros_last():
    sound = makeEmptySound(22050)
    assert getSampleValueAt(sound, 22049) == 0

def test_makeEmptySound_small_size():
    sound = makeEmptySound(1)
    assert getNumSamples(sound) == 1
    assert getSampleValueAt(sound, 0) == 0




def test_combined_write_then_read():
    sound = makeEmptySound(22050)
    setSampleValueAt(sound, 0, 100)
    assert getSampleValueAt(sound, 0) == 100

def test_combined_write_negative():
    sound = makeEmptySound(22050)
    setSampleValueAt(sound, 0, -100)
    assert getSampleValueAt(sound, 0) == -100

def test_combined_write_max():
    sound = makeEmptySound(22050)
    setSampleValueAt(sound, 0, 32767)
    assert getSampleValueAt(sound, 0) == 32767

def test_combined_write_min():
    sound = makeEmptySound(22050)
    setSampleValueAt(sound, 0, -32768)
    assert getSampleValueAt(sound, 0) == -32768

def test_combined_write_zero_after_nonzero():
    sound = makeEmptySound(22050)
    setSampleValueAt(sound, 0, 500)
    setSampleValueAt(sound, 0, 0)
    assert getSampleValueAt(sound, 0) == 0

def test_combined_overwrite_value():
    sound = makeEmptySound(22050)
    setSampleValueAt(sound, 0, 100)
    setSampleValueAt(sound, 0, 200)
    setSampleValueAt(sound, 0, 300)
    assert getSampleValueAt(sound, 0) == 300

def test_combined_write_multiple_positions():
    sound = makeEmptySound(22050)
    setSampleValueAt(sound, 0, 100)
    setSampleValueAt(sound, 100,200)
    setSampleValueAt(sound, 22049, 300)
    assert getSampleValueAt(sound, 0)     == 100
    assert getSampleValueAt(sound, 100)   == 200
    assert getSampleValueAt(sound, 22049) == 300

def test_combined_write_does_not_affect_neighbors():
    sound = makeEmptySound(22050)
    setSampleValueAt(sound, 0, 999)
    assert getSampleValueAt(sound, 1) == 0

def test_combined_write_last_index():
    sound = makeEmptySound(22050)
    setSampleValueAt(sound,22049, 777)
    assert getSampleValueAt(sound, 22049) == 777

def test_combined_full_fill_and_verify():
    sound = makeEmptySound(10)
    for i in range(10):
        setSampleValueAt(sound, i, i * 10)
    for i in range(10):
        assert getSampleValueAt(sound, i) == i * 10

