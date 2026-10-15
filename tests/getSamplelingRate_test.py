import pytest
import os
from mediaComp import *

SOUND_PATH = os.path.join(os.path.dirname(__file__), 'sources', 'a.wav')


def test_getSamplingRate_returns_int():
    sound = makeSound(SOUND_PATH)
    assert isinstance(getSamplingRate(sound), int)

def test_getSamplingRate_is_positive():
    sound = makeSound(SOUND_PATH)
    assert getSamplingRate(sound) > 0

def test_getSamplingRate_consistent():
    sound = makeSound(SOUND_PATH)
    assert getSamplingRate(sound) == getSamplingRate(sound)

def test_getSamplingRate_same_file_loaded_twice():
    sound1 = makeSound(SOUND_PATH)
    sound2 = makeSound(SOUND_PATH)
    assert getSamplingRate(sound1) == getSamplingRate(sound2)
    
    

def test_getSamplingRate_common_value():
    sound = makeSound(SOUND_PATH)
    assert getSamplingRate(sound) in [8000, 11025, 22050, 44100, 48000]

def test_getSamplingRate_empty_sound_default():
    sound = makeEmptySound(22050)
    assert getSamplingRate(sound) == 22050

def test_getSamplingRate_matches_duration_and_num_samples():
    sound = makeSound(SOUND_PATH)
    expected = getNumSamples(sound) / getDuration(sound)
    assert abs(getSamplingRate(sound) - expected) <= 1
    
    
    

def test_getSamplingRate_not_affected_by_sample_modification():
    sound = makeSound(SOUND_PATH)
    original_rate = getSamplingRate(sound)
    setSampleValueAt(sound, 0, 999)
    assert getSamplingRate(sound) == original_rate

def test_getSamplingRate_empty_sound_small():
    sound = makeEmptySound(2205)
    assert getSamplingRate(sound) == 22050

def test_getSamplingRate_empty_sound_large():
    sound = makeEmptySound(44100)
    assert getSamplingRate(sound) == 22050
