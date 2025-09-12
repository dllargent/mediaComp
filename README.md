# mediaComp 
MediaComp is a free and open-source conversion of the multimedia library JES4PY by Mark Guzdial to Python 3. It utilizes multiple popular libraries to provide an abstraction of manipulating sounds, images, and colors. 

## Installation
Before installing mediaComp, verify that Python is installed on your device. To find out, open a command prompt or terminal and type:

```python --version ```

If a message like "Python 3.12.5" is displayed it means Python is installed and you can install mediaComp. If an error message occurs, check the official [Python website](https://www.python.org/) to download it. 

To install our package run:

```python -m pip install mediaComp```

## Help

If you are new to mediaComp you should be able to start faily easily. Our abstraction make the functionality of the library intuitive. Full documentation can be found on our [GitHub](https://github.com/dllargent/mediaComp).

## Credits
Thank you so everyone who has contributed to this library.
- Dave Largent
- Jason Yoder
- CJ Fulciniti
- Santos Pena

## Dependencies
MediaComp is strongly dependent on several libraries. Most of the these will install with the package, ***however*** Windows users will need to download and install the Visual Studio Build Tools for C/C++ development (see documentation).

| Dependency | Version |
| :-----:| :-----: |
| wxPython | > 4/2/0 |
| pillow | > 11/0/0 |
| pygame | > 2/5/0 |
| simpleaudio | >= 1.0.3 |
| matplotlib | >= 3.10.0 |

## License
This package is distributed under GPL 3.0-or-later, which can be found in our GitHub repository in ```LICENSE```. This means you can basically use mediaComp in any project you want. Any changes or additions made the package must also be released with a compatible license.