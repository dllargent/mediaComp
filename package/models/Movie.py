from .Picture import Picture
from ..core import makePicture

class Movie(object):
    def __init__(self):  
        self.frames = []
        self.dir = None

    def addFrame(self, frame):
        self.frames.append(frame)
        self.dir = None

    def __len__(self):
        return len(self.frames)

    def __str__(self):
        return "Movie, frames: " + str(len(self))

    def __repr__(self):
        return "Movie, frames: " + str(len(self))

    def __getitem__(self, item):
        return self.frames[item]

    def writeFramesToDirectory(self, directory):
        import FrameSequencer
        fs = FrameSequencer(directory)
        for frameindex in range(0, len(self.frames)):
            fs.addFrame(Picture(self.frames[frameindex]))
        self.dir = directory

    def play(self):
        list = []
        for f in self.frames:
            list.add(makePicture(f))
        MoviePlayer(list).playMovie()