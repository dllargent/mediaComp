# mediaComp: a multimedia library for Python 3 
MediaComp is a free and open-source multimedia library for Python 3 which enables the easy manipulation of images and sounds. It utilizes popular libraries to provide an abstraction of manipulating sounds, images, and colors, by abstracting the complexity into easy-to-use function calls.

## History
MediaComp is a conversion of the multimedia library originally developed and released by Mark Guzdial & Barbara Ericson for use with their _Introduction to Computing and Programming in Python: A multimedia Approach_ book (last edition ISBN 978-0-13-402554-4). It is based on Python 3, whereas the Guzdial/Ericson (G/E) version was based on Jython 2.7. Our implementation is based on Gordon College's [JES4PY](https://github.com/gordon-cs/JES4py "Gordon College's JESPY GitHub repository") conversion, which implemented a subset of the original G/E multimedia library features so they could be used in Python 3. Their goal was, and ours is, to provide the pedagogical assets of the G/E multimedia library without requiring Jython or needing to use the JES IDE. While mediaComp is still a subset of the G/E implementation, it provides added functionality when compared to JESPY.

MediaComp is a conversion of only the media computation multimedia library, and does not include [JES](https://github.com/gatech-csl/jes), the Jython Environment for Students, which is an educational IDE used in the Media Computation curriculum developed by Guzdial and Ericson. More details on the curriculum are available at http://www.mediacomputation.org/.

## Installation
Before installing mediaComp, verify that Python is installed on your device. To find out, open a command prompt or terminal and type:

```python --version ```

If a message like "Python 3.12.5" is displayed it means Python is installed and you can install mediaComp. If an error message occurs, check the official [Python website](https://www.python.org/) to download it. 

To install our package run:

```python -m pip install mediaComp[gui]```

## Help

Even if you are new to mediaComp you should be able to start faily easily. Our abstractions make the functionality of the library intuitive. Full documentation can be found on our [GitHub](https://github.com/dllargent/mediaComp/).

## Credits
Thank you to everyone who has contributed to this library.
- Dave Largent (mentor)
- Jason Yoder
- CJ Fulciniti
- Santos Pena

## Dependencies
MediaComp is strongly dependent on several libraries. Most of the these will install with the package, ***however*** to make sure you get wxPython with the package, install it with 
```pip install mediaComp[gui]```.

| Dependency | Version |
| :-----:| :-----: |
| wxPython | > 4.2.0 |
| pillow | > 11.0.0 |
| pygame | > 2.5.0 |
| matplotlib | >= 3.10.0 |
| numpy | >= 2.2.1 |
| sounddevice | >= 0.5.2 |

## Tested IDEs

MediaComp is primarily used in the [Thonny IDE](https://thonny.org/), but has been used in [VSCode](https://code.visualstudio.com/) and [JetBrains PyCharm](https://www.jetbrains.com/pycharm/) as well. If you encounter an issue using any of the three IDE's, [submit an issue](https://github.com/dllargent/mediaComp/issues)! 

## License
This package is distributed under GPL 3.0-or-later, which can be found in our GitHub repository in ```LICENSE```. This means you can basically use mediaComp in any project you want. Any changes or additions made the package must also be released with a compatible license.
