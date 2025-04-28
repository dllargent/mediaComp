import threading
import os, random, time
import pygame.midi
from ..models.Sound import Sound
from ..models.Sample import Sample
from ..models.Samples import Samples
from .utils import getShortPath
import matplotlib.pyplot as plt
import tkinter as tk

def samplesToSound(samples):
    maxIndex = max([getIndex(s) for s in samples])
    newSound = makeEmptySound(maxIndex + 1, int(getSamplingRate(samples[0].getSound())))
    for s in samples:
        x = getIndex(s)
        setSampleValueAt(newSound, x, getSampleValue(s))
    return newSound

def makeSound(filename):
    global mediaFolder
    if not isinstance(filename, str):
        return samplesToSound(filename)
    if not os.path.isabs(filename):
        filename = mediaFolder + filename
    if not os.path.isfile(filename):
        print("There is no file at " + filename)
        raise ValueError
    return Sound(filename)

def makeEmptySound(numSamples, samplingRate=Sound.SAMPLE_RATE):
    numSamples = int(numSamples)
    if numSamples <= 0 or samplingRate <= 0:
        print("makeEmptySound(numSamples[, samplingRate]): numSamples and samplingRate must each be greater than 0")
        raise ValueError
    if (numSamples / samplingRate) > 600:
        print("makeEmptySound(numSamples[, samplingRate]): Created sound must be less than 600 seconds")
        raise ValueError
    return Sound(numSamples, samplingRate)

def makeEmptySoundBySeconds(seconds, samplingRate=Sound.SAMPLE_RATE):
    if seconds <= 0 or samplingRate <= 0:
        print("makeEmptySoundBySeconds(numSamples[, samplingRate]): numSamples and samplingRate must each be greater than 0")
        raise ValueError
    if seconds > 600:
        print("makeEmptySoundBySeconds(numSamples[, samplingRate]): Created sound must be less than 600 seconds")
        raise ValueError
    return Sound(seconds * samplingRate, samplingRate)

def duplicateSound(sound):
    if not isinstance(sound, Sound):
        print("duplicateSound(sound): Input is not a sound")
        raise ValueError
    return Sound(sound)


def getSamples(sound):
    if not isinstance(sound, Sound):
        print("getSamples(sound): Input is not a sound")
        raise ValueError
    return Samples.getSamples(sound)


def play(sound):
    if not isinstance(sound, Sound):
        print("play(sound): Input is not a sound")
        raise ValueError
    sound.play()


def blockingPlay(sound):
    if not isinstance(sound, Sound):
        print("blockingPlay(sound): Input is not a sound")
        raise ValueError
    sound.blockingPlay()

def threadedPlay(sound):
    if not isinstance(sound, Sound):
        print("threadedPlay(sound): Input is not a sound")
        raise ValueError
    threading.Thread(target = lambda: sound.blockingPlayMix(), daemon = True).start()


def stopPlaying(sound):
    if not isinstance(sound, Sound):
        print("stopPlaying(sound): Input is not a sound")
        raise ValueError
    sound.stopPlaying()


def playAtRate(sound, rate):
    if not isinstance(sound, Sound):
        print("playAtRate(sound,rate): First input is not a sound")
        raise ValueError
    sound.playAtRateDur(rate, sound.getLength())


def playAtRateDur(sound, rate, dur):
    if not isinstance(sound, Sound):
        print("playAtRateDur(sound,rate,dur): First input is not a sound")
        raise ValueError
    sound.playAtRateDur(rate, dur)


def playInRange(sound, start, stop):
    if not isinstance(sound, Sound):
        print("playInRange(sound,start,stop): First input is not a sound")
        raise ValueError
    sound.playAtRateInRange(
        1, start - Sound._SoundIndexOffset, stop - Sound._SoundIndexOffset)


def blockingPlayInRange(sound, start, stop):
    if not isinstance(sound, Sound):
        print("blockingPlayInRange(sound,start,stop): First input is not a sound")
        raise ValueError
    sound.blockingPlayAtRateInRange(
        1, start - Sound._SoundIndexOffset, stop - Sound._SoundIndexOffset)


def playAtRateInRange(sound, rate, start, stop):
    if not isinstance(sound, Sound):
        print("playAtRateInRAnge(sound,rate,start,stop): First input is not a sound")
        raise ValueError
    sound.playAtRateInRange(
        rate, start - Sound._SoundIndexOffset, stop - Sound._SoundIndexOffset)


def blockingPlayAtRateInRange(sound, rate, start, stop):
    if not isinstance(sound, Sound):
        print("blockingPlayAtRateInRange(sound,rate,start,stop): First input is not a sound")
        raise ValueError
    sound.blockingPlayAtRateInRange(
        rate, start - Sound._SoundIndexOffset, stop - Sound._SoundIndexOffset)
    
def getSamplingRate(sound):
    if not isinstance(sound, Sound):
        print("getSamplingRate(sound): Input is not a sound")
        raise ValueError
    return sound.getSamplingRate()


def setSampleValueAt(sound, index, value):
    if not isinstance(sound, Sound):
        print("setSampleValueAt(sound,index,value): First input is not a sound")
        raise ValueError
    if index < Sound._SoundIndexOffset:
        print("You asked for the sample at index: " + str(index) + ".  This number is less than " + str(Sound._SoundIndexOffset) + ".  Please try" + " again using an index in the range [" + str(Sound._SoundIndexOffset) + "," + str(getLength(sound) - 1 + Sound._SoundIndexOffset) + "].")
        raise ValueError
    if index > getLength(sound) - 1 + Sound._SoundIndexOffset:
        print("You are trying to access the sample at index: " + str(index) + ", but the last valid index is at " + str(getLength(sound) - 1 + Sound._SoundIndexOffset))
        raise ValueError
    sound.setSampleValue(index - Sound._SoundIndexOffset, int(value))


def getSampleValueAt(sound, index):
    if not isinstance(sound, Sound):
        print("getSampleValueAt(sound,index): First input is not a sound")
        raise ValueError
    if index < Sound._SoundIndexOffset:
        print("You asked for the sample at index: " + str(index) + ".  This number is less than " + str(Sound._SoundIndexOffset) + ".  Please try" + " again using an index in the range [" + str(Sound._SoundIndexOffset) + "," + str(getLength(sound) - 1 + Sound._SoundIndexOffset) + "].")
        raise ValueError
    if index > getLength(sound) - 1 + Sound._SoundIndexOffset:
        print("You are trying to access the sample at index: " + str(index) + ", but the last valid index is at " + str(getLength(sound) - 1 + Sound._SoundIndexOffset))
        raise ValueError
    return sound.getSampleValue(index - Sound._SoundIndexOffset)


def getSampleObjectAt(sound, index):
    if not isinstance(sound, Sound):
        print("getSampleObjectAt(sound,index): First input is not a sound")
        raise ValueError
    if index < Sound._SoundIndexOffset:
        print("You asked for the sample at index: " + str(index) + ".  This number is less than " + str(Sound._SoundIndexOffset) + ".  Please try" + " again using an index in the range [" + str(Sound._SoundIndexOffset) + "," + str(getLength(sound) - 1 + Sound._SoundIndexOffset) + "].")
        raise ValueError
    if index > getLength(sound) - 1 + Sound._SoundIndexOffset:
        print("You are trying to access the sample at index: " + str(index) + ", but the last valid index is at " + str(getLength(sound) - 1 + Sound._SoundIndexOffset))
        raise ValueError
    return Sample(sound, index - Sound._SoundIndexOffset)


def setSampleValue(sample, value):
    if not isinstance(sample, Sample):
        print("setSample(sample,value): First input is not a sample")
        raise ValueError
    if value > 32767:
        value = 32767
    elif value < -32768:
        value = -32768
    return sample.setValue(int(value))


def getSampleValue(sample):
    if not isinstance(sample, Sample):
        print("getSample(sample): Input is not a sample")
        raise ValueError
    return sample.getValue()

def getSound(sample):
    if not isinstance(sample, Sample):
        print("getSound(sample): Input is not a sample")
        raise ValueError
    return sample.getSound()

def getLength(sound):
    if not isinstance(sound, Sound):
        print("getLength(sound): Input is not a sound")
        raise ValueError
    return sound.getLength()


def getNumSamples(sound):
    return getLength(sound)


def getDuration(sound):
    if not isinstance(sound, Sound):
        print("getDuration(sound): Input is not a sound")
        raise ValueError
    return sound.getLength() / sound.getSamplingRate()


def writeSoundTo(sound, filename):
    global mediaFolder
    if not os.path.isabs(filename):
        filename = mediaFolder + filename
    if not isinstance(sound, Sound):
        print("writeSoundTo(sound,filename): First input is not a sound")
        raise ValueError
    sound.writeToFile(filename)


def randomSamples(someSound, number):
    samplelist = []
    samples = getSamples(someSound)
    for count in range(number):
        samplelist.append(random.choice(samples))
    if(isinstance(samplesToSound(samplelist), Sound)):
        soundTool

def getIndex(sample):
    return int(str(sample).split()[2])

def playNote(note, duration, intensity=64):
    if not (0 <= note <= 127):
        raise ValueError("playNote(): Note must be between 0 and 127.")
    if not (0 <= intensity <= 127):
        raise ValueError("playNote(): Intensity must be between 0 and 127.")
    pygame.midi.init()	
    try:
        port = pygame.midi.get_default_output_id()	
        midi_out = pygame.midi.Output(port)
        midi_out.note_on(note, intensity)	
        time.sleep(duration / 1000.0)	
        midi_out.note_off(note, intensity)	
    finally:
        del midi_out	
        pygame.midi.quit()

def soundTool(sound):
    if isinstance(sound, Sound):
        samplesList = list(map(getSampleValue,getSamples(sound)))
        try:
            fileName = getShortPath(sound.getFileName())
            if fileName == "":
                fileName = "No file name"
        except:
            fileName = "No file name"
        plt.figure(num=fileName)
        samplingRate = int(getSamplingRate(sound))
        plotTitle = fileName + "  (" + str(samplingRate) + " samples/second)"
        plt.title(plotTitle)
        plt.subplots_adjust(left=0.15, bottom=.15)
        plt.plot(range(1,1+len(samplesList)),samplesList)
        plt.axline((0,0),slope=0, color='k')
        plt.xlabel("Sample index (time)")
        plt.ylabel("Sample value (volume)")
        plt.show()
    else:
        print("openSound(sound): Input is not a sound.")
        raise ValueError