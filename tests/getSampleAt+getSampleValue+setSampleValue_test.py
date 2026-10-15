import pytest
import os
from mediaComp import *

SOUND_PATH = os.path.join(os.path.dirname(__file__), 'sources', 'a.wav')

def test_getSampleAt_returns_sample_object():
    sound = makeSound(SOUND_PATH)
    sample = getSampleAt(sound, 0)
    assert not isinstance(sample, (int, float))

def test_getSampleAt_first_index():
    sound = makeSound(SOUND_PATH)
    sample = getSampleAt(sound, 0)
    assert sample is not None

def test_getSampleAt_last_index():
    sound = makeSound(SOUND_PATH)
    last_index = getNumSamples(sound) - 1
    sample = getSampleAt(sound, last_index)
    assert sample is not None

def test_getSampleAt_consistent():
    sound = makeSound(SOUND_PATH)
    s1 = getSampleAt(sound, 0)
    s2 = getSampleAt(sound, 0)
    assert getSampleValue(s1) == getSampleValue(s2)

def test_getSampleAt_empty_sound():
    sound = makeEmptySound(22050)
    sample = getSampleAt(sound, 100)
    assert sample is not None




def test_getSampleAt_getSampleValue_returns_int():
    sound = makeSound(SOUND_PATH)
    sample = getSampleAt(sound, 0)
    assert isinstance(getSampleValue(sample), int)

def test_getSampleAt_getSampleValue_in_valid_range():
    sound = makeSound(SOUND_PATH)
    sample = getSampleAt(sound, 0)
    val = getSampleValue(sample)
    assert -32768 <= val <= 32767

def test_getSampleAt_getSampleValue_empty_is_zero():
    sound = makeEmptySound(22050)
    sample = getSampleAt(sound, 0)
    assert getSampleValue(sample) == 0

def test_getSampleAt_getSampleValue_matches_getSampleValueAt():
    sound = makeSound(SOUND_PATH)
    sample = getSampleAt(sound, 0)
    assert getSampleValue(sample) == getSampleValueAt(sound, 0)




def test_getSampleAt_setSampleValue_changes_value():
    sound = makeEmptySound(22050)
    sample = getSampleAt(sound, 0)
    setSampleValue(sample, 100)
    assert getSampleValue(sample) == 100

def test_getSampleAt_setSampleValue_negative():
    sound = makeEmptySound(22050)
    sample = getSampleAt(sound, 0)
    setSampleValue(sample, -100)
    assert getSampleValue(sample) == -100

def test_getSampleAt_setSampleValue_max():
    sound = makeEmptySound(22050)
    sample = getSampleAt(sound, 0)
    setSampleValue(sample, 32767)
    assert getSampleValue(sample) == 32767

def test_getSampleAt_setSampleValue_min():
    sound = makeEmptySound(22050)
    sample = getSampleAt(sound, 0)
    setSampleValue(sample, -32768)
    assert getSampleValue(sample) == -32768
 


def test_combined_getSampleAt_set_get():
    sound = makeEmptySound(22050)
    sample = getSampleAt(sound, 0)
    setSampleValue(sample, 512)
    assert getSampleValue(sample) == 512

def test_combined_modify_reflects_in_getSampleValueAt():
    sound = makeEmptySound(22050)
    sample = getSampleAt(sound, 0)
    setSampleValue(sample, 888)
    assert getSampleValueAt(sound, 0) == 888

def test_combined_modify_multiple_positions():
    sound = makeEmptySound(22050)
    for i, val in enumerate([100, 200, 300]):
        setSampleValue(getSampleAt(sound, i), val)
    for i, val in enumerate([100, 200, 300]):
        assert getSampleValue(getSampleAt(sound, i)) == val

def test_combined_modify_does_not_affect_neighbors():
    sound = makeEmptySound(22050)
    setSampleValue(getSampleAt(sound, 0), 999)
    assert getSampleValue(getSampleAt(sound, 1)) == 0
