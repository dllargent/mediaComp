import pytest
import os
from mediaComp import *

SOUND_PATH = os.path.join(os.path.dirname(__file__), 'sources', 'a.wav')

def test_makeSound_returns_object():
    sound = makeSound(SOUND_PATH)
    assert sound is not None

def test_makeSound_has_positive_duration():
    sound = makeSound(SOUND_PATH)
    assert getDuration(sound) > 0

def test_makeSound_has_positive_num_samples():
    sound = makeSound(SOUND_PATH)
    assert getNumSamples(sound) > 0

def test_makeSound_has_positive_sampling_rate():
    sound = makeSound(SOUND_PATH)
    assert getSamplingRate(sound) > 0
    
    
    

def test_makeSound_sampling_rate_is_standard():
    sound = makeSound(SOUND_PATH)
    standard_rates = [8000, 11025, 22050, 44100]
    assert getSamplingRate(sound) in standard_rates

def test_makeSound_num_samples_matches_duration():
    sound = makeSound(SOUND_PATH)
    expected = int(getDuration(sound) * getSamplingRate(sound))
    actual= getNumSamples(sound)
    assert abs(actual - expected) <= 1
    
    

def test_makeSound_two_loads_same_duration():
    sound1 = makeSound(SOUND_PATH)
    sound2 = makeSound(SOUND_PATH)
    assert getDuration(sound1) == getDuration(sound2)

def test_makeSound_two_loads_same_num_samples():
    sound1 = makeSound(SOUND_PATH)
    sound2 = makeSound(SOUND_PATH)
    assert getNumSamples(sound1) == getNumSamples(sound2)

def test_makeSound_two_loads_are_independent():
    sound1 = makeSound(SOUND_PATH)
    sound2 = makeSound(SOUND_PATH)
    original_value = getSampleValueAt(sound2, 0)
    setSampleValueAt(sound1, 0, 0)
    assert getSampleValueAt(sound2, 0) == original_value
    
    

def test_makeSound_invalid_path_raises_error():
    with pytest.raises(Exception):
        makeSound(r'C:\not\exist\fake.wav')
