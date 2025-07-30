import threading
import os, random, time
import pygame.midi
from ..models.Sound import Sound
from ..models.Sample import Sample
from ..models.Samples import Samples
from .utils import getShortPath
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from ..models.SoundExplorer import SoundExplorer

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

def makeEmptySound(numSamples, samplingRate=Sound.SAMPLE_RATE, filename=None):
    numSamples = int(numSamples)
    if numSamples <= 0 or samplingRate <= 0:
        print("makeEmptySound(numSamples[, samplingRate]): numSamples and samplingRate must each be greater than 0")
        raise ValueError
    if (numSamples / samplingRate) > 600:
        print("makeEmptySound(numSamples[, samplingRate]): Created sound must be less than 600 seconds")
        raise ValueError
    return Sound(numSamples, samplingRate, filename)

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
    threading.Thread(target = lambda: sound.blockingPlay(), daemon = True).start()


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
        print("You asked for the sample at index: " + str(index) + ".  This number is less than " + str(Sound._SoundIndexOffset) + ".  Please try" + " again using an index in the range [" + str(Sound._SoundIndexOffset) + "," + str(getNumSamples
        (sound) - 1 + Sound._SoundIndexOffset) + "].")
        raise ValueError
    if index > getNumSamples(sound) - 1 + Sound._SoundIndexOffset:
        print("You are trying to access the sample at index: " + str(index) + ", but the last valid index is at " + str(getNumSamples(sound) - 1 + Sound._SoundIndexOffset))
        raise ValueError
    sound.setSampleValue(index - Sound._SoundIndexOffset, int(value))


def getSampleValueAt(sound, index):
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

def getNumSamples(sound):
    if not isinstance(sound, Sound):
        print("getLength(sound): Input is not a sound")
        raise ValueError
    return sound.getLength()

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
    # if isinstance(sound, Sound):
    #     samplesList = list(map(getSampleValue,getSamples(sound)))
    #     try:
    #         fileName = getShortPath(sound.getFileName())
    #         if fileName == "":
    #             fileName = "No file name"
    #     except:
    #         fileName = "No file name"
    #     plt.figure(num=fileName)
    #     samplingRate = int(getSamplingRate(sound))
    #     plotTitle = fileName + "  (" + str(samplingRate) + " samples/second)"
    #     plt.title(plotTitle)
    #     plt.subplots_adjust(left=0.15, bottom=.15)
    #     plt.plot(range(1,1+len(samplesList)),samplesList)
    #     plt.axline((0,0),slope=0, color='k')
    #     plt.xlabel("Sample index (time)")
    #     plt.ylabel("Sample value (volume)")
    #     plt.show()
    # else:
    #     print("openSound(sound): Input is not a sound.")
    #     raise ValueError
    
    soundGUI(createSoundPlot(sound), sound)
    #explore = SoundExplorer(sound)
    #explore.show()
    
def createSoundPlot(sound):
    try:
        samplesList = list(map(getSampleValue, getSamples(sound)))
        fileName = getShortPath(sound.getFileName())
        if fileName == "":
            fileName = "No file name"
    except:
        fileName = "No file name"
    figure, ax = plt.subplots( figsize= (8,6))
    plotTitle = fileName + "  (" + str(int(getSamplingRate(sound))) + " samples/second)"
    figure.canvas.manager.set_window_title(plotTitle)
    waveform = ax
    waveform.set_title(plotTitle)
    sampleIndices = range(0, len(samplesList))
    waveform.plot(sampleIndices, samplesList, color = "mediumseagreen", linewidth = 0.75)
    waveform.grid(True, linestyle = "--", alpha = 0.7)

    waveform.axline((0, 0), slope=0, color='k')
    waveform.set_xlabel("Sample index (time)")
    waveform.set_xlim(0, len(sampleIndices))
    waveform.set_ylabel("Sample value (volume)")
    waveform.set_ylim(-32768, 32767)

    return figure

def soundGUI(soundPlot, sound:Sound):
    window = tk.Tk()
    window.title("Sound Explorer")
    window.geometry("900x700")
    window.configure(bg = "#9A9999")
    
    # Bring window to front immediately
    window.lift()
    window.attributes('-topmost', True)
    window.after_idle(lambda: window.attributes('-topmost', False))
    window.focus_force()

    def play_sound():
        try:
            # Ensure pygame mixer is properly initialized with correct parameters
            pygame.mixer.quit()  # Clean slate
            size = -16 if sound.sampleWidth == 2 else -8  # Signed 16-bit or 8-bit
            pygame.mixer.init(frequency=int(sound.getSamplingRate()/2), 
                            size=size, 
                            channels=sound.numChannels, 
                            buffer=512)
            
            soundObj = pygame.mixer.Sound(buffer=sound.buffer)
            soundObj.play()
            
        except Exception as e:
            print(f"Playback error: {e}")
            try:
                if sound.soundMix:
                    sound.soundMix.play()
            except:
                print("Both playback methods failed")
    
    def on_closing():
        try:
            if sound.soundMix:
                sound.soundMix.stop()
            sound.stopPlaying()
        except:
            pass
        window.quit()
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_closing)
    
    button = tk.Button(window, width=12, text="Play", bg="gray", 
                      command=play_sound)
    button.pack()
    
    frame = tk.Frame(window, bg = "#9A9999")
    canvas = FigureCanvasTkAgg(figure=soundPlot, master=frame)
    frame.pack(padx = 10, pady = 10, fill = "both") 
    canvas.get_tk_widget().pack()
    canvas.draw()
    
    window.mainloop()
