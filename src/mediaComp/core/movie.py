from ..models.Movie import Movie
import os


def playMovie(movie) -> None:
    if isinstance(movie, Movie):
        movie.play()
    else:
        print("playMovie( movie ): Input is not a Movie")
        raise ValueError


def writeQuicktime(movie, destPath, framesPerSec=16) -> None:
    if not (isinstance(movie, Movie)):
        print("writeQuicktime(movie, path[, framesPerSec]): First input is not a Movie")
        raise ValueError
    if framesPerSec <= 0:
        print("writeQuicktime(movie, path[, framesPerSec]): Frame rate must be a positive number")
        raise ValueError
    movie.writeQuicktime(destPath, framesPerSec)


def writeAVI(movie, destPath, framesPerSec=16) -> None:
    if not (isinstance(movie, Movie)):
        print("writeAVI(movie, path[, framesPerSec]): First input is not a Movie")
        raise ValueError
    if framesPerSec <= 0:
        print("writeAVI(movie, path[, framesPerSec]): Frame rate must be a positive number")
        raise ValueError
    movie.writeAVI(destPath, framesPerSec)


def makeMovie() -> Movie:
    return Movie()


def makeMovieFromInitialFile(filename) -> Movie:
    import re
    movie = Movie()
    global mediaFolder
    filename = filename.replace('/', os.sep)
    sep_location = filename.rfind(os.sep)
    if(-1 == sep_location):
        filename = mediaFolder + filename

    movie.directory = filename[:(filename.rfind(os.sep))]
    movie.init_file = filename[(filename.rfind(os.sep)) + 1:]
    regex = re.compile('[0-9]+')
    file_regex = regex.sub('.*', movie.init_file)

    for item in sorted(os.listdir(movie.directory)):
        if re.match(file_regex, item):
            movie.addFrame(movie.directory + os.sep + item)

    return movie


def addFrameToMovie(a, b) -> None:
    frame = None
    movie = None
    if a.__class__ == Movie:
        movie = a
        frame = b
    else:
        movie = b
        frame = a

    if not (isinstance(movie, Movie) and isinstance(frame, str)):
        print("addFrameToMovie(frame, movie): frame is not a string or movie is not a Movie object")
        raise ValueError

    movie.addFrame(frame)


def writeFramesToDirectory(movie, directory=None) -> None:
    if not isinstance(movie, Movie):
        print("writeFramesToDirectory(movie[, directory]): movie is not a Movie object")
        raise ValueError

    if directory == None:
        directory = user.home

    movie.writeFramesToDirectory(directory)