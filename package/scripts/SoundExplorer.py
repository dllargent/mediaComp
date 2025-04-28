import matplotlib as plt
from matplotlib import colormaps
import numpy as np
from matplotlib.widgets import Button
from mediaNew import *
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

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

def soundGUI(soundPlot, sound):
    """Here we display the sound in a GUI window, using tkinter.
    Matplotlib creates the waveform which is passed to this function."""
    #first we call and config the window itself
    window = tk.Tk()
    window.title("Sound Explorer")
    window.geometry("900x700")
    window.configure(bg = "#9A9999")
    #packing our play button here to blockingPlay sound
    button = tk.Button(window, width=12 ,text="Play Sound", bg="gray",
                       command=lambda: threadedPlay(sound))
    button.pack()
    #Here we set up a frame for the plot
    frame = tk.Frame(window, bg = "#9A9999")
    #which is passed here under master
    canvas = FigureCanvasTkAgg(figure=soundPlot, master=frame)
    frame.pack(padx = 10, pady = 10, fill = "both") #Here we bond it with our library
    canvas.get_tk_widget().pack() #embed
    canvas.draw()
    #cmap?
    window.mainloop()
