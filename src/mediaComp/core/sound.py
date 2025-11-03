import threading
import os, random, time
import pygame.midi
from ..models.Sound import Sound
from ..models.Sample import Sample
from ..models.Samples import Samples
from ..models.SoundExplorer import SoundExplorer

def getSampleAt(sound, index) -> Sample:
    if not isinstance(sound, Sound):
        print("getSampleAt(sound,index): First input is not a sound")
        raise ValueError
    if index < Sound._SoundIndexOffset:
        print("You asked for the sample at index: " + str(index) + ".  This number is less than " + str(Sound._SoundIndexOffset) + ".  Please try" + " again using an index in the range [" + str(Sound._SoundIndexOffset) + "," + str(getNumSamples
        (sound) - 1 + Sound._SoundIndexOffset) + "].")
        raise ValueError
    if index > getNumSamples(sound) - 1 + Sound._SoundIndexOffset:
        print("You are trying to access the sample at index: " + str(index) + ", but the last valid index is at " + str(getNumSamples(sound) - 1 + Sound._SoundIndexOffset))
        raise ValueError
    return Sample(sound, index - Sound._SoundIndexOffset)

def samplesToSound(samples) -> Sound:
    maxIndex = max([getIndex(s) for s in samples])
    newSound = makeEmptySound(maxIndex + 1, int(getSamplingRate(samples[0].getSound())))
    for s in samples:
        x = getIndex(s)
        setSampleValueAt(newSound, x, getSampleValue(s))
    return newSound

def makeSound(filename) -> Sound:
    global mediaFolder
    if not isinstance(filename, str):
        return samplesToSound(filename)
    if not os.path.isabs(filename):
        filename = mediaFolder + filename
    if not os.path.isfile(filename):
        print("There is no file at " + filename)
        raise ValueError
    return Sound(filename)

def makeEmptySound(numSamples, samplingRate=Sound.SAMPLE_RATE, filename=None) -> Sound:
    numSamples = int(numSamples)
    if numSamples <= 0 or samplingRate <= 0:
        print("makeEmptySound(numSamples[, samplingRate]): numSamples and samplingRate must each be greater than 0")
        raise ValueError
    if (numSamples / samplingRate) > 600:
        print("makeEmptySound(numSamples[, samplingRate]): Created sound must be less than 600 seconds")
        raise ValueError
    return Sound(numSamples, samplingRate, filename)

def makeEmptySoundBySeconds(seconds, samplingRate=Sound.SAMPLE_RATE) -> Sound:
    if seconds <= 0 or samplingRate <= 0:
        print("makeEmptySoundBySeconds(numSamples[, samplingRate]): numSamples and samplingRate must each be greater than 0")
        raise ValueError
    if seconds > 600:
        print("makeEmptySoundBySeconds(numSamples[, samplingRate]): Created sound must be less than 600 seconds")
        raise ValueError
    return Sound(seconds * samplingRate, samplingRate)

def duplicateSound(sound) -> Sound:
    if not isinstance(sound, Sound):
        print("duplicateSound(sound): Input is not a sound")
        raise ValueError
    return Sound(sound)


def getSamples(sound) -> Samples:
    if not isinstance(sound, Sound):
        print("getSamples(sound): Input is not a sound")
        raise ValueError
    return Samples.getSamples(sound)


def play(sound: Sound, isBlocking: bool = False) -> None:
    if not isinstance(sound, Sound):
        print("play(sound): Input is not a sound")
        raise ValueError
    sound.play(isBlocking)

def threadedPlay(sound) -> None:
    if not isinstance(sound, Sound):
        print("threadedPlay(sound): Input is not a sound")
        raise ValueError
    threading.Thread(target = lambda: sound.blockingPlay(), daemon = True).start()


def stopPlaying(sound) -> None:
    if not isinstance(sound, Sound):
        print("stopPlaying(sound): Input is not a sound")
        raise ValueError
    sound.stopPlaying()


def playAtRate(sound, rate, isBlocking: bool = False) -> None:
    if not isinstance(sound, Sound):
        print("playAtRate(sound,rate): First input is not a sound")
        raise ValueError
    if(rate < 1000 or rate > 150000):
        print("The rate {} is not valid. It must be between 1000 and 150000".format(rate))
        raise ValueError
    sound.playAtRateDur(rate, sound.getLength(), isBlocking)


def playAtRateDur(sound, rate, dur, isBlocking: bool = False) -> None:
    if not isinstance(sound, Sound):
        print("playAtRateDur(sound,rate,dur): First input is not a sound")
        raise ValueError
    if(rate < 1000 or rate > 150000):
        print("The rate {} is not valid. It must be between 1000 and 150000".format(rate))
        raise ValueError
    sound.playAtRateDur(rate, dur, isBlocking)


def playInRange(sound, start, stop, isBlocking: bool = False) -> None:
    if not isinstance(sound, Sound):
        print("playInRange(sound,start,stop): First input is not a sound")
        raise ValueError
    sound.playRange(1, start - Sound._SoundIndexOffset, stop - Sound._SoundIndexOffset, isBlocking)


def playAtRateInRange(sound, rate, start, stop, isBlocking) -> None:
    if not isinstance(sound, Sound):
        print("playAtRateInRAnge(sound,rate,start,stop): First input is not a sound")
        raise ValueError
    sound.playAtRateInRange(rate, start - Sound._SoundIndexOffset, stop - Sound._SoundIndexOffset, isBlocking)

    
def getSamplingRate(sound) -> int:
    if not isinstance(sound, Sound):
        print("getSamplingRate(sound): Input is not a sound")
        raise ValueError
    return sound.getSamplingRate()


def setSampleValueAt(sound, index, value) -> None:
    if not isinstance(sound, Sound):
        print("setSampleValueAt(sound,index,value): First input is not a sound")
        raise ValueError
    if index < Sound._SoundIndexOffset:
        print("You asked for the sample at index: " + str(index) + ".  This number is less than " + str(Sound._SoundIndexOffset) + ".  Please try" + " again using an index in the range [" + str(Sound._SoundIndexOffset) + "," + str(getNumSamples
        (sound) - 1 + Sound._SoundIndexOffset) + "].")
        raise ValueError
    if index > getNumSamples(sound) - 1 + Sound._SoundIndexOffset:
        print("You are trying to access the sample at index: " + str(index) + ", but the last valid index is at " + str(getNumSamples(sound) - 1 + Sound._SoundIndexOffset))
        raise ValueError
    sound.setSampleValue(index - Sound._SoundIndexOffset, int(value))


def getSampleValueAt(sound, index) -> int:
    if not isinstance(sound, Sound):
        print("getSampleValueAt(sound,index): First input is not a sound")
        raise ValueError
    if index < Sound._SoundIndexOffset:
        print("You asked for the sample at index: " + str(index) + ".  This number is less than " + str(Sound._SoundIndexOffset) + ".  Please try" + " again using an index in the range [" + str(Sound._SoundIndexOffset) + "," + str(getNumSamples(sound) - 1 + Sound._SoundIndexOffset) + "].")
        raise ValueError
    if index > getNumSamples(sound) - 1 + Sound._SoundIndexOffset:
        print("You are trying to access the sample at index: " + str(index) + ", but the last valid index is at " + str(getNumSamples(sound) - 1 + Sound._SoundIndexOffset))
        raise ValueError
    return sound.getSampleValue(index - Sound._SoundIndexOffset)


def setSampleValue(sample, value) -> None:
    if not isinstance(sample, Sample):
        print("setSample(sample,value): First input is not a sample")
        raise ValueError
    if value > 32767:
        value = 32767
    elif value < -32768:
        value = -32768
    return sample.setValue(int(value))


def getSampleValue(sample) -> int:
    if not isinstance(sample, Sample):
        print("getSample(sample): Input is not a sample")
        raise ValueError
    return sample.getValue()

def getSound(sample) -> Sound:
    if not isinstance(sample, Sample):
        print("getSound(sample): Input is not a sample")
        raise ValueError
    return sample.getSound()

def getNumSamples(sound) -> int:
    if not isinstance(sound, Sound):
        print("getLength(sound): Input is not a sound")
        raise ValueError
    return sound.getLength()

def getDuration(sound) -> float:
    if not isinstance(sound, Sound):
        print("getDuration(sound): Input is not a sound")
        raise ValueError
    return sound.getLength() / sound.getSamplingRate()


def writeSoundTo(sound, filename) -> None:
    global mediaFolder
    if not os.path.isabs(filename):
        filename = mediaFolder + filename
    if not isinstance(sound, Sound):
        print("writeSoundTo(sound,filename): First input is not a sound")
        raise ValueError
    sound.writeToFile(filename)


def randomSamples(someSound, number) -> Sound:
    samplelist = []
    samples = getSamples(someSound)
    for count in range(number):
        samplelist.append(random.choice(samples))
    if(isinstance(samplesToSound(samplelist), Sound)):
        soundTool

def getIndex(sample) -> int:
    return int(str(sample).split()[2])

def playNote(note, duration, intensity=64) -> None:
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

def soundTool(sound) -> None:
    explore = SoundExplorer(sound)
    explore.show()