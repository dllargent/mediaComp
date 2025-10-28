from .SoundSample import SoundSample
import wave
import os
#import simpleaudio as sa
import pygame
import threading

import sounddevice as sd
import numpy as np

class Sound:
    MAX_NEG = -32768
    MAX_POS = 32767
    SAMPLE_RATE = 22050
    NUM_BITS_PER_SAMPLE = 16
    _SoundIndexOffset = 0

    def __init__(self, sound, sampleRate=22050, filename=None):
        """Construct new sound object
        
        If first passed parameter is the name of a WAV file, then read
        the file.

        If first passed parameter is an int representing a number of
        frames, then construct Sound object of the specified length.
        This sound will simply consist of an empty byte array and an
        AudioFileFormat with the following values:
            AudioFileFormat.Type.WAVE</code>
            22.05K sampling rate
            16 bit sample
            1 channel
            signed PCM encoding
            small-endian byte order
        Note that no new sound file is created, we only represent the
        sound with a buffer and the AudioFileFormat.  If a file is
        desired, then the method writeToFile(filename) must be called
        on this newly created sound.

        Parameters
        ----------
        sound : str
            the filename of containing a sound in WAV format
        sound : int
            the number of samples in the sound
        sound : Sound
            a preexisting Sound object
        sampleRate : int
            the frame rate for the sound
        """
        if isinstance(sound, str):
            self.filename = filename if filename is not None else sound
            self.lock = threading.Lock()
            self.is_playing = False
            
            with wave.open(self.filename, 'rb') as waveRead:
                self.numFrames = waveRead.getnframes()
                self.numChannels = waveRead.getnchannels()
                self.sampleWidth = waveRead.getsampwidth()
                self.sampleRate = waveRead.getframerate()
                self.buffer = bytearray(waveRead.readframes(self.numFrames))
                
        elif isinstance(sound, int):
            self.filename = filename if filename is not None else ''
            self.numFrames = sound
            self.lock = threading.Lock()
            self.is_playing = False
            self.numChannels = 1
            self.sampleWidth = int(self.NUM_BITS_PER_SAMPLE / 8)
            self.sampleRate = sampleRate
            numBytes = self.numChannels * self.numFrames * self.sampleWidth
            self.buffer = bytearray([0] * numBytes)
            
        elif isinstance(sound, Sound):
            self.filename = filename if filename is not None else sound.filename
            self.numFrames = sound.numFrames
            self.lock = threading.Lock()
            self.is_playing = False
            self.numChannels = sound.numChannels
            self.sampleWidth = sound.sampleWidth
            self.sampleRate = sound.sampleRate
            self.buffer = sound.buffer.copy()
        
        size = int(8 * self.sampleWidth)
        try:
            pygame.mixer.init(frequency=self.sampleRate, size=size, channels=self.numChannels)
        except pygame.error as e:
            print(f"Warning: Could not initialize pygame mixer: {e}")
        
        self.soundMix = None
        try:
            if self.filename and os.path.isfile(self.filename):
                self.soundMix = pygame.mixer.Sound(self.filename)
            else:
                self.soundMix = pygame.mixer.Sound(buffer=self.buffer)
        except:
            try:
                self.soundMix = pygame.mixer.Sound(buffer=self.buffer)
            except:
                try:
                    simple_buffer = bytearray([0] * (self.sampleRate * self.sampleWidth * self.numChannels))
                    self.soundMix = pygame.mixer.Sound(buffer=simple_buffer)
                except:
                    print("Could not create any pygame Sound object")
                    self.soundMix = None
        
    def __str__(self):
        """Return string representation of this sound

        Returns
        -------
        str
            representation of this sound
        """
        output = "Sound file: {} number of samples: {}".format(self.filename, self.numFrames)
        return output

    def __repr__(self):
        """Return string representation of this sound

        Returns
        -------
        str
            representation of this sound
        """
        return self.__str__()

    # ----------------------- accessors --------------------------------------

    def getBuffer(self):
        """Returns this sound's associated buffer

        Returns
        -------
        arr
            The sounds buffer(i.e. an array representaion of the sound)
        """
        return self.buffer

    def getSamplingRate(self):
        """Return this sound's sampling rate

        Returns
        -------
        int
            the sampling rate
        """
        return self.sampleRate

    def asArray(self):
        """Returns an array representation of the sound

        Returns
        -------
        arr
            The sounds buffer(i.e. an array representaion of the sound)
        """
        return self.buffer

    def getPlaybacks(self):
        """Returns an array of all the current sound's playbacks

        Returns
        -------
        list
            array of all the current sounds playbacks
        """
        return self.playbacks

    def getChannels(self):
        """Return sounds number of channels

        Returns
        -------
        int
            number of channels
        """
        return self.numChannels
        
    def getFileName(self):
        """Return sounds file name

        Returns
        -------
        string
            name of associated file
        """
        return self.filename

    def getFrame(self, frameNum):
        """Obtains all the data from a specified frame in the audio data

        Parameters
        ----------
        frameNum : int
            the index of the frame to access

        Returns
        -------
        bytearray
            the array containing all of the bytes in frame
        """
        if (frameNum >= self.numFrames):
            print("The index {}, does not exist. The last valid index is {}".format(frameNum, self.numFrames-1))
            
        frameSize = int(len(self.buffer)/self.numFrames)
        theFrame = bytearray(frameSize)
        for i in range(frameSize):
            theFrame[i] = self.buffer[frameNum * frameSize + i]
        return theFrame
    
    def getLengthInFrames(self):
        """Obtains number of sample frames in the audio data

        Returns
        -------
        int
            the number of sample frames of audio data in the sound
        """
        return self.numFrames

    def getNumSamples(self):
        """Returns the number of samples in this sound

        Returns
        -------
        int
            the number of sample frames
        """
        return self.getLengthInFrames()

    def getSample(self, frameNum):
        """Create and return a SoundSample object for the given frame number

        Parameters
        ----------
        frameNum : int
            the frame from which to retrieve the SoundSample object

        Returns
        -------
        SoundSample
            a SoundSample object for this frame number
        """
        return SoundSample(self, frameNum)

    def getSamples(self):
        """Method to create and return an array of SoundSample objects

        Returns
        -------
        list of SoundSample
            the array of SoundSample objects
        """
        samples = []
        for i in range(self.numFrames):
            samples.append(SoundSample(self, i))
        return samples
    
    def getSampleValueAt(self, index):
        """Get the sample at the passed index and handle any SoundExceptions

        Parameters
        ----------
        index : int
            the desired index

        Returns
        -------
        int
            the sample value
        """
        try:
            value = self.getSampleValue(index)
        except:
            raise(IndexError("The index {} is not valid for this sound".format(index)))
        return value
    
    def getSampleValue(self, frameNum):
        """Sets the value of the sample at the indicated frame
        
        If this is a mono sound, obtains the single sample contained
        within this frame, else obtains the first (left) sample
        contained in the specified frame.

        Parameters
        ----------
        frameNum : int
            the index of the frame to access

        Returns
        -------
        int
            integer representation of the bytes contained within frame
        """
        n = frameNum * self.sampleWidth * self.numChannels
        m = n + self.sampleWidth
        return int.from_bytes(self.buffer[n:m], byteorder='little', signed=True)    

    def getLeftSample(self, frameNum):
        """Obtains the left sample contained at the specified frame

        Parameters
        ----------
        frameNum : int
            the index of the frame to access

        Returns
        -------
        int
            integer representation of the bytes contained in the specified frame.
        """
        if not self.isStereo():
            print("Sound is not stereo, cannot access left value")
        return self.getSampleValue(frameNum)

    def getRightSample(self, frameNum):
        """Obtains the right sample contained at the specified frame

        Parameters
        ----------
        frameNum : int
            the index of the frame to access

        Returns
        -------
        int
            integer representation of the bytes contained in the specified frame.
        """
        if not self.isStereo():
            print("Sound is not stereo, cannot access right value")
        else:
            n = frameNum * self.sampleWidth * self.numChannels + self.sampleWidth
            m = n + self.sampleWidth
            return int.from_bytes(self.buffer[n:m], byteorder='little', signed=True)    

    def getLengthInBytes(self):
        """Obtains the length of this sound in bytes
        
        Note, that this number is not neccessarily the same as the length of
        this sound's file in bytes

        Returns
        -------
        int
            the sound length in bytes
        """
        return len(self.buffer)

    def getLength(self):
        """Return the length of the sound as the number of samples

        Returns
        -------
        int
            the length of the sound as the number of samples
        """
        return self.getNumSamples()

    def isStereo(self):
        """Method to check if a sound is stereo (2 channel) or not

        Returns
        -------
        bool
            True if stereo else False
        """
        return self.numChannels != 1

    # ----------------------- modifiers --------------------------------------

    def setBuffer(self, newBuffer):
        """Changes the buffer assoiciated with the current sound to the (newBuffer)

        Parameters
        ----------
        newBuffer : int
            the length of the buffer that will replace (self.buffer)
        newBuffer : bytearray
            the byte array that (self.buffer) is being replaced with
        """
        if isinstance(newBuffer, int):
            self.buffer = bytearray(newBuffer)
        elif isinstance(newBuffer, bytearray):
            self.buffer = newBuffer.copy() 

    def setFrame(self, frameNum, frame):
        """Changes the value of each byte of the specified frame

        Parameters
        ----------
        frameNum : int
            the index of the frame to change
        frame : byte array
            the bytes that will be copied into this sound's buffer
        """
        if frameNum >= self.numFrames:
            print("The frame number {} does not exist".format(frameNum))
            print("The last valud frame number is {}".format(self.numFrames-1))
        else:
            for i in range(self.sampleWidth):
                self.buffer[frameNum * self.sampleWidth + i] = frame[i]

    def setSampleValueAt(self, index, value):
        """Method to set the sample value at the specified index

        Parameters
        ----------
        index : int
            the index
        value : int or float
            the new value
        """
        try:
            self.setSampleValue(index, int(value))
        except:
            raise(IndexError("The index {} is not valid for this sound".format(index)))

    def setSampleValue(self, frameNum, value):
        """Sets the value of the sample found at the specified frame
        
        If this sound has more than one channel, then we default to setting
        only the first (left) sample.  Values outside of the range
        [MAX_NEG, MAX_POS] are silently clipped to be within that range.
    
        Parameters
        ----------
        frameNum : int
            the index of the frame where the sample should be changed
        value : int
           the new sample value
        """
        n = frameNum * self.sampleWidth * self.numChannels
        m = n + self.sampleWidth
        value = max(min(value, self.MAX_POS), self.MAX_NEG)
        self.buffer[n:m] = value.to_bytes(self.sampleWidth,
                                          byteorder='little',
                                          signed=True)

    def setLeftSample(self, frameNum, value):
        """Set the left sample value in a stereo sample
        
        Parameters
        ----------
        frameNum : int
            the index of the frame where the sample should be changed
        value : int
            an integer representation of the new sample
        """
        if not self.isStereo():
            print("Sound is not stereo, cannot set left value")
        else:
            self.setSampleValue(frameNum, value)

    def setRightSample(self, frameNum, value):
        """Set the right sample value in a stereo sample
        
        Values outside of the range [MAX_NEG, MAX_POS] are silently clipped
        to be within that range.

        Parameters
        ----------
        frameNum : int
            the index of the frame where the sample should be changed
        value : int
            an integer representation of the new sample
        """
        if not self.isStereo():
            print("Sound is not stereo, cannot set right value")
        else:
            n = frameNum * self.sampleWidth * self.numChannels + self.sampleWidth
            m = n + self.sampleWidth
            value = max(min(value, self.MAX_POS), self.MAX_NEG)
            self.buffer[n:m] = value.to_bytes(self.sampleWidth,
                                              byteorder='little',
                                              signed=True)

    def setFileName(self, filename):
        """Set sound's file name

        Parameters
        ----------
        filename : string
            filename to assign to this sound
        """
        self.filename = filename

    # ------------------------ methods ---------------------------------------

    def play(self, isBlocking=False):
        """Play a sound - nonblocking
        """
        sd.play(np.frombuffer(self.buffer, dtype=np.int16), samplerate=self.sampleRate)
        if isBlocking:
            sd.wait()

    def playRange(self, start, end, isBlocking=False):
        dtype = np.int16 if self.sampleWidth == 2 else np.uint8 
        audio_array = np.frombuffer(self.buffer, dtype=dtype)

        # Reshape if stereo/multichannel
        if self.numChannels > 1:
            audio_array = audio_array.reshape(-1, self.numChannels)

        # Slice frames
        segment = audio_array[start:end]
        sd.play(segment, samplerate=self.sampleRate)
        if isBlocking:
            sd.wait()

    def playAtRateDur(self, rate, duration, isBlocking=False):
        
        dtype = np.int16 if self.sampleWidth == 2 else np.uint8  # common cases
        audio_array = np.frombuffer(self.buffer, dtype=dtype)

        # Reshape if stereo/multichannel
        if self.numChannels > 1:
            audio_array = audio_array.reshape(-1, self.numChannels)

        # Slice frames
        segment = audio_array[0:duration]
        sd.play(segment, samplerate=rate)
        if isBlocking:
            sd.wait()

    def stopPlaying(self):
        """Stop playback of all currently playing sounds
        """
        #while len(self.playbacks) > 0:
        #    self.playbacks.pop().stop()
        sd.stop()

    def convert(self, mp3File, wavFile):
        print("this method isn't implemented.")
    
    def reportIndexException(self, index):
        """Method to report an index exception for this sound

        Parameters
        ----------
        index : int
            the index
        """
        print("The index {} isn't valid for this sound".format(index))


    # ------------------------ File I/O ---------------------------------------

    def loadFromFile(self, inFileName):
        """Resets the fields of this sound so that it now represents the
           sound in the specified file.  If successful, the fileName variable
           is updated such that it is equivalent to the passed in file
 
        Parameters
        ----------
        inFileName : str
            the name of the file to read the sound in from
        """
        self.filename = inFileName
        waveRead = wave.open(self.filename, 'rb')
        self.numFrames = waveRead.getnframes()
        self.numChannels = waveRead.getnchannels()
        self.sampleWidth = waveRead.getsampwidth()
        self.sampleRate = waveRead.getframerate()
        self.buffer = bytearray(waveRead.readframes(self.numFrames))
        waveRead.close()

    def write(self, fileName):
        """Write the sound to a wav file and throw an error if it can't be written
 
        Parameters
        ----------
        fileName : str
            the name of the file to write the sound to
        """
        try:
            self.writeToFile(fileName)
        except IOError:
            print("Couldn't write file to " + fileName)

    def writeToFile(self, outFileName):
        """Write the sound to a wav file
 
        Parameters
        ----------
        outFileName : str
            the name of the file to write the sound to
        """

        file = wave.open(outFileName, "wb")
        file.setnframes(self.numFrames)
        file.setnchannels(self.numChannels)
        file.setsampwidth(self.sampleWidth)
        file.setframerate(self.sampleRate)
        file.writeframes(self.buffer)
        file.close()

    def setSoundExplorer(self, soundExplorer):
        self.soundExplorer = soundExplorer