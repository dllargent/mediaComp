import pytest
import os
from mediaComp import *

SOUND_PATH = os.path.join(os.path.dirname(__file__), 'sources', 'a.wav')


def test_getSound_returns_sound_object():
    sound = makeSound(SOUND_PATH)
    sample = getSampleAt(sound, 0)
    result = getSound(sample)
    assert result is not None

def test_getSound_not_returns_primitive():
    sound = makeSound(SOUND_PATH)
    sample = getSampleAt(sound, 0)
    result = getSound(sample)
    assert not isinstance(result, (int, float, str))

def test_getSound_consistent():
    sound = makeSound(SOUND_PATH)
    sample = getSampleAt(sound, 0)
    assert getNumSamples(getSound(sample)) == getNumSamples(getSound(sample))

def test_getSound_empty_sound():
    sound = makeEmptySound(22050)
    sample = getSampleAt(sound, 0)
    result = getSound(sample)
    assert result is not None





def test_combined_getSound_matches_original_numsamples():
    sound = makeSound(SOUND_PATH)
    sample = getSampleAt(sound, 0)
    retrieved = getSound(sample)
    assert getNumSamples(retrieved) == getNumSamples(sound)

def test_combined_getSound_matches_original_samplingrate():
    sound = makeSound(SOUND_PATH)
    sample = getSampleAt(sound, 0)
    retrieved = getSound(sample)
    assert getSamplingRate(retrieved) == getSamplingRate(sound)

def test_combined_getSound_matches_original_duration():
    sound = makeSound(SOUND_PATH)
    sample = getSampleAt(sound, 0)
    retrieved = getSound(sample)
    assert getDuration(retrieved) == getDuration(sound)

def test_combined_getSound_sample_value_consistent():
    sound = makeSound(SOUND_PATH)
    sample = getSampleAt(sound, 0)
    retrieved = getSound(sample)
    assert getSampleValueAt(retrieved, 0) == getSampleValueAt(sound, 0)

def test_combined_different_indices_same_sound():
    sound = makeSound(SOUND_PATH)
    sample_first = getSampleAt(sound, 0)
    sample_last  = getSampleAt(sound, getNumSamples(sound) - 1)
    assert getNumSamples(getSound(sample_first)) == getNumSamples(getSound(sample_last))

def test_combined_empty_sound_numsamples():
    sound = makeEmptySound(22050)
    sample = getSampleAt(sound, 0)
    retrieved = getSound(sample)
    assert getNumSamples(retrieved) == getNumSamples(sound)

def test_combined_modify_then_getSound_reflects_change():
    sound = makeEmptySound(22050)
    sample = getSampleAt(sound, 0)
    setSampleValue(sample, 888)
    retrieved = getSound(sample)
    assert getSampleValueAt(retrieved, 0) == 888
