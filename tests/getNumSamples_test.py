import pytest
import os
from mediaComp import *

SOUND_PATH = os.path.join(os.path.dirname(__file__), 'sources', 'a.wav')


def test_getNumSamples_returns_int():
    sound = makeSound(SOUND_PATH)
    assert isinstance(getNumSamples(sound), int)

def test_getNumSamples_is_positive():
    sound = makeSound(SOUND_PATH)
    assert getNumSamples(sound) > 0

def test_getNumSamples_consistent():
    sound = makeSound(SOUND_PATH)
    assert getNumSamples(sound) == getNumSamples(sound)

def test_getNumSamples_same_file_loaded_twice():
    sound1 = makeSound(SOUND_PATH)
    sound2 = makeSound(SOUND_PATH)
    assert getNumSamples(sound1) == getNumSamples(sound2)
    
    

def test_getNumSamples_matches_duration_and_rate():
    sound = makeSound(SOUND_PATH)
    expected = getDuration(sound) * getSamplingRate(sound)
    assert abs(getNumSamples(sound) - expected) <= 1

def test_getNumSamples_empty_sound_exact():
    sound = makeEmptySound(22050)
    assert getNumSamples(sound) == 22050
    
    

def test_getNumSamples_empty_sound_small():
    sound = makeEmptySound(2205)
    assert getNumSamples(sound) == 2205

def test_getNumSamples_larger_empty_sound():
    sound_short = makeEmptySound(2205)
    sound_long  = makeEmptySound(22050)
    assert getNumSamples(sound_short) < getNumSamples(sound_long)

def test_getNumSamples_not_affected_by_sample_modification():
    sound = makeSound(SOUND_PATH)
    original_num = getNumSamples(sound)
    setSampleValueAt(sound, 0, 999)
    assert getNumSamples(sound) == original_num

def test_getNumSamples_proportional_to_duration():
    sound_half = makeEmptySound(11025)
    sound_full = makeEmptySound(22050)
    assert getNumSamples(sound_full) == 2 * getNumSamples(sound_half)
