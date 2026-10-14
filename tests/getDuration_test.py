import pytest
import os
from mediaComp import *

SOUND_PATH = os.path.join(os.path.dirname(__file__), 'sources', 'a.wav')


def test_getDuration_returns_float():
    sound = makeSound(SOUND_PATH)
    assert isinstance(getDuration(sound), float)

def test_getDuration_is_positive():
    sound = makeSound(SOUND_PATH)
    assert getDuration(sound) > 0

def test_getDuration_consistent():
    sound = makeSound(SOUND_PATH)
    assert getDuration(sound) == getDuration(sound)

def test_getDuration_same_file_loaded_twice():
    sound1 = makeSound(SOUND_PATH)
    sound2 = makeSound(SOUND_PATH)
    assert getDuration(sound1) == getDuration(sound2)



def test_getDuration_matches_num_samples_and_rate():
    sound = makeSound(SOUND_PATH)
    expected = getNumSamples(sound) / getSamplingRate(sound)
    assert abs(getDuration(sound) - expected) <= 0.01

def test_getDuration_empty_sound_short():
    sound_short = makeEmptySound(2205)  
    sound_long = makeEmptySound(22050) 
    assert getDuration(sound_short) < getDuration(sound_long)
    
    

def test_getDuration_empty_sound_1_second():
    sound = makeEmptySound(22050)
    assert abs(getDuration(sound) - 1.0) <= 0.01

def test_getDuration_empty_sound_2_seconds():
    sound = makeEmptySound(44100)
    assert abs(getDuration(sound) - 2.0) <= 0.01

def test_getDuration_not_affected_by_sample_modification():
    sound = makeSound(SOUND_PATH)
    original_duration = getDuration(sound)
    setSampleValueAt(sound, 0, 999)
    assert getDuration(sound) == original_duration

def test_getDuration_proportional_to_num_samples():
    sound_half = makeEmptySound(11025)
    sound_full = makeEmptySound(22050)
    assert abs(getDuration(sound_full) - 2 * getDuration(sound_half)) <= 0.01
