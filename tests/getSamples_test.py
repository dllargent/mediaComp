import pytest
import os
from mediaComp import *

SOUND_PATH = os.path.join(os.path.dirname(__file__), 'sources', 'a.wav')


def test_getSamples_returns_list():
    sound = makeSound(SOUND_PATH)
    assert isinstance(getSamples(sound), list)

def test_getSamples_length_matches_getNumSamples():
    sound = makeSound(SOUND_PATH)
    assert len(getSamples(sound)) == getNumSamples(sound)

def test_getSamples_not_empty():
    sound = makeSound(SOUND_PATH)
    assert len(getSamples(sound)) > 0

def test_getSamples_empty_sound():
    sound = makeEmptySound(22050)
    assert len(getSamples(sound)) == 22050




def test_getSampleValue_returns_int():
    sound = makeSound(SOUND_PATH)
    samples = getSamples(sound)
    assert isinstance(getSampleValue(samples[0]), int)

def test_getSampleValue_in_valid_range():
    sound = makeSound(SOUND_PATH)
    samples = getSamples(sound)
    val = getSampleValue(samples[0])
    assert -32768 <= val <= 32767

def test_getSampleValue_empty_sound_is_zero():
    sound = makeEmptySound(22050)
    samples = getSamples(sound)
    assert getSampleValue(samples[0]) == 0

def test_getSampleValue_consistent():
    sound = makeSound(SOUND_PATH)
    samples = getSamples(sound)
    assert getSampleValue(samples[0]) == getSampleValue(samples[0])




def test_setSampleValue_changes_value():
    sound = makeEmptySound(22050)
    samples = getSamples(sound)
    setSampleValue(samples[0], 100)
    assert getSampleValue(samples[0]) == 100

def test_setSampleValue_negative_value():
    sound = makeEmptySound(22050)
    samples = getSamples(sound)
    setSampleValue(samples[0], -100)
    assert getSampleValue(samples[0]) == -100

def test_setSampleValue_max_value():
    sound = makeEmptySound(22050)
    samples = getSamples(sound)
    setSampleValue(samples[0], 32767)
    assert getSampleValue(samples[0]) == 32767

def test_setSampleValue_min_value():
    sound = makeEmptySound(22050)
    samples = getSamples(sound)
    setSampleValue(samples[0], -32768)
    assert getSampleValue(samples[0]) == -32768





def test_combined_get_set_get():
    sound = makeEmptySound(22050)
    samples = getSamples(sound)
    setSampleValue(samples[0], 512)
    assert getSampleValue(samples[0]) == 512

def test_combined_modify_multiple_samples():
    sound = makeEmptySound(22050)
    samples = getSamples(sound)
    setSampleValue(samples[0], 100)
    setSampleValue(samples[1], 200)
    setSampleValue(samples[2], 300)
    assert getSampleValue(samples[0]) == 100
    assert getSampleValue(samples[1]) == 200
    assert getSampleValue(samples[2]) == 300

def test_combined_modify_does_not_affect_other_samples():
    sound = makeEmptySound(22050)
    samples = getSamples(sound)
    setSampleValue(samples[0], 999)
    assert getSampleValue(samples[1]) == 0

def test_combined_samples_reflect_in_sound():
    sound = makeEmptySound(22050)
    samples = getSamples(sound)
    setSampleValue(samples[0], 777)
    assert getSampleValueAt(sound, 0) == 777
