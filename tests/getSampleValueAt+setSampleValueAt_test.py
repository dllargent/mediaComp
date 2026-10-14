import pytest
import os
from mediaComp import *

SOUND_PATH = os.path.join(os.path.dirname(__file__), 'sources', 'a.wav')

 

def test_getSampleValueAt_returns_int():
    sound = makeSound(SOUND_PATH)
    assert isinstance(getSampleValueAt(sound, 0), int)

def test_getSampleValueAt_in_valid_range():
    sound = makeSound(SOUND_PATH)
    val = getSampleValueAt(sound, 0)
    assert -32768 <= val <= 32767

def test_getSampleValueAt_first_index():
    sound = makeSound(SOUND_PATH)
    val = getSampleValueAt(sound, 0)
    assert val is not None

def test_getSampleValueAt_last_index():
    sound = makeSound(SOUND_PATH)
    last_index = getNumSamples(sound) - 1
    val = getSampleValueAt(sound, last_index)
    assert -32768 <= val <= 32767

def test_getSampleValueAt_consistent():
    sound = makeSound(SOUND_PATH)
    assert getSampleValueAt(sound, 0) == getSampleValueAt(sound, 0)

def test_getSampleValueAt_empty_sound_is_zero():
    sound = makeEmptySound(22050)
    assert getSampleValueAt(sound, 0) == 0

def test_getSampleValueAt_empty_sound_middle_is_zero():
    sound = makeEmptySound(22050)
    assert getSampleValueAt(sound, 11025) == 0




def test_setSampleValueAt_changes_value():
    sound = makeEmptySound(22050)
    setSampleValueAt(sound, 0, 100)
    assert getSampleValueAt(sound, 0) == 100

def test_setSampleValueAt_negative_value():
    sound = makeEmptySound(22050)
    setSampleValueAt(sound, 0, -100)
    assert getSampleValueAt(sound, 0) == -100

def test_setSampleValueAt_max_value():
    sound = makeEmptySound(22050)
    setSampleValueAt(sound, 0, 32767)
    assert getSampleValueAt(sound, 0) == 32767

def test_setSampleValueAt_min_value():
    sound = makeEmptySound(22050)
    setSampleValueAt(sound, 0, -32768)
    assert getSampleValueAt(sound, 0) == -32768

def test_setSampleValueAt_zero_value():
    sound = makeEmptySound(22050)
    setSampleValueAt(sound, 0, 999)
    setSampleValueAt(sound, 0, 0)
    assert getSampleValueAt(sound, 0) == 0

def test_setSampleValueAt_last_index():
    sound = makeEmptySound(22050)
    last_index = getNumSamples(sound) - 1
    setSampleValueAt(sound, last_index, 500)
    assert getSampleValueAt(sound, last_index) == 500
 
 
 
 

def test_combined_set_then_get():
    sound = makeEmptySound(22050)
    setSampleValueAt(sound, 0, 512)
    assert getSampleValueAt(sound, 0) == 512

def test_combined_overwrite_value():
    sound = makeEmptySound(22050)
    setSampleValueAt(sound, 0, 100)
    setSampleValueAt(sound, 0, 200)
    assert getSampleValueAt(sound, 0) == 200

def test_combined_modify_multiple_positions():
    sound = makeEmptySound(22050)
    setSampleValueAt(sound, 0, 100)
    setSampleValueAt(sound, 1, 200)
    setSampleValueAt(sound, 2, 300)
    assert getSampleValueAt(sound, 0) == 100
    assert getSampleValueAt(sound, 1) == 200
    assert getSampleValueAt(sound, 2) == 300

def test_combined_modify_does_not_affect_neighbors():
    sound = makeEmptySound(22050)
    setSampleValueAt(sound, 0, 999)
    assert getSampleValueAt(sound, 1) == 0

def test_combined_real_sound_overwrite():
    sound = makeSound(SOUND_PATH)
    setSampleValueAt(sound, 0, 777)
    assert getSampleValueAt(sound, 0) == 777
