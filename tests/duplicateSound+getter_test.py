import pytest
import os
from mediaComp import *

SOUND_PATH = os.path.join(os.path.dirname(__file__), 'sources', 'a.wav')

def test_duplicateSound_returns_object():
    sound = makeSound(SOUND_PATH)
    dup = duplicateSound(sound)
    assert dup is not None

def test_duplicateSound_is_different_object():
    sound = makeSound(SOUND_PATH)
    dup = duplicateSound(sound)
    assert dup is not sound

def test_duplicateSound_empty_sound():
    sound = makeEmptySound(22050)
    dup = duplicateSound(sound)
    assert dup is not None



def test_duplicateSound_numsamples_equal():
    sound = makeSound(SOUND_PATH)
    dup = duplicateSound(sound)
    assert getNumSamples(dup) == getNumSamples(sound)

def test_duplicateSound_empty_numsamples_equal():
    sound = makeEmptySound(22050)
    dup = duplicateSound(sound)
    assert getNumSamples(dup) == getNumSamples(sound)



def test_duplicateSound_samplingrate_equal():
    sound = makeSound(SOUND_PATH)
    dup = duplicateSound(sound)
    assert getSamplingRate(dup) == getSamplingRate(sound)

def test_duplicateSound_empty_samplingrate_equal():
    sound = makeEmptySound(22050)
    dup = duplicateSound(sound)
    assert getSamplingRate(dup) == getSamplingRate(sound)

 
 
def test_duplicateSound_duration_equal():
    sound = makeSound(SOUND_PATH)
    dup = duplicateSound(sound)
    assert getDuration(dup) == getDuration(sound)

def test_duplicateSound_empty_duration_equal():
    sound = makeEmptySound(22050)
    dup = duplicateSound(sound)
    assert getDuration(dup) == getDuration(sound)

 
 
def test_duplicateSound_first_sample_equal():
    sound = makeSound(SOUND_PATH)
    dup = duplicateSound(sound)
    assert getSampleValueAt(dup, 0) == getSampleValueAt(sound, 0)

def test_duplicateSound_last_sample_equal():
    sound = makeSound(SOUND_PATH)
    dup = duplicateSound(sound)
    last = getNumSamples(sound) - 1
    assert getSampleValueAt(dup, last) == getSampleValueAt(sound, last)

def test_duplicateSound_empty_all_samples_zero():
    sound = makeEmptySound(22050)
    dup = duplicateSound(sound)
    assert getSampleValueAt(dup, 0) == 0
    assert getSampleValueAt(dup, 11025) == 0
 
 
 
def test_duplicateSound_modify_dup_not_affect_original():
    sound = makeEmptySound(22050)
    dup = duplicateSound(sound)
    setSampleValueAt(dup, 0, 999)
    assert getSampleValueAt(sound, 0) == 0

def test_duplicateSound_modify_original_not_affect_dup():
    sound = makeEmptySound(22050)
    dup = duplicateSound(sound)
    setSampleValueAt(sound, 0, 999)
    assert getSampleValueAt(dup, 0) == 0

def test_duplicateSound_dup_numsamples_unchanged_after_modify():
    sound = makeSound(SOUND_PATH)
    dup = duplicateSound(sound)
    setSampleValueAt(dup, 0, 100)
    assert getNumSamples(dup) == getNumSamples(sound)
