from typing import Optional
from abc import ABC, abstractmethod
import threading
import tkinter as tk
from .Sound import Sound
from .PixelColor import Color

class MouseMotionListener(ABC):
    @abstractmethod
    def mouse_dragged(self, event):
        pass
    
    @abstractmethod
    def mouse_moved(self, event):
        pass

class ActionListener(ABC):
    @abstractmethod
    def action_performed(self, event):
        pass

class MouseListener(ABC):
    @abstractmethod
    def mouse_clicked(self, event):
        pass
    
    @abstractmethod
    def mouse_pressed(self, event):
        pass
    
    @abstractmethod
    def mouse_released(self, event):
        pass

class LineListener(ABC):
    @abstractmethod
    def update(self, event):
        pass

class SamplingPanel(tk.Frame,):
    """Class to display the sound wave."""
    
    def __init__(self, parent, sound_explorer: 'SoundExplorer'):
        super().__init__(parent)
        self.sound_explorer = sound_explorer
        self.points = []
        
        if sound_explorer.debug:
            print(f"Creating new sampling panel:")
            print(f"\tsampleWidth: {sound_explorer.sample_width}")
            print(f"\tsampleHeight: {sound_explorer.sample_height}")
        
        self.config(
            bg=sound_explorer.BACKGROUND_COLOR,
            width=sound_explorer.sample_width,
            height=sound_explorer.sample_height
        )
        
        # Create canvas for drawing
        self.canvas = tk.Canvas(
            self,
            width=sound_explorer.sample_width,
            height=sound_explorer.sample_height,
            bg=sound_explorer.BACKGROUND_COLOR,
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Bind mouse events to canvas
        self.canvas.bind('<Motion>', sound_explorer.mouse_moved)
        self.canvas.bind('<Button-1>', sound_explorer.mouse_clicked)
        self.canvas.bind('<ButtonPress-1>', sound_explorer.mouse_pressed)
        self.canvas.bind('<ButtonRelease-1>', sound_explorer.mouse_released)
        self.canvas.bind('<B1-Motion>', sound_explorer.mouse_dragged)
        
        self.create_wave_form()
    
    def create_wave_form(self):
        """Create the sound wave visualization."""
        sound: Sound = self.sound_explorer.sound
        sample_width = self.sound_explorer.sample_width
        sample_height = self.sound_explorer.sample_height
        frames_per_pixel = self.sound_explorer.frames_per_pixel
        
        # Get max value for this sample size
        try:
            # Try different methods to get sample format info
            max_value = 32768  # Default for 16-bit
            
            # Try to get format info if available
            if hasattr(sound, 'get_audio_file_format'):
                format_info = sound.get_audio_file_format()
                sample_size_bits = format_info.get_sample_size_in_bits()
            else:
                # Default to 16-bit
                sample_size_bits = 16
                
            if sample_size_bits == 8:
                max_value = 2 ** 7
            elif sample_size_bits == 16:
                max_value = 2 ** 15
            elif sample_size_bits == 24:
                max_value = 2 ** 23
            elif sample_size_bits == 32:
                max_value = 2 ** 31
            else:
                max_value = 32768  # Default fallback
                
        except Exception as ex:
            self.sound_explorer.catch_exception(ex)
            max_value = 32768  # Use default if we can't determine
        
        self.points.clear()
        
        for pixel in range(sample_width):
            try:
                sample_index = int(pixel * frames_per_pixel)
                if sample_index < sound.getLengthInFrames():
                    sample_value = sound.getSampleValue(sample_index)
                    # Normalize the sample value to fit in the display
                    y = (sample_height // 2) - (sample_value * (sample_height // 2) / max_value)
                    # Clamp y to valid range
                    y = max(0, min(sample_height, y))
                    self.points.append((pixel, y))
                else:
                    # If we're past the end of the sound, draw at center line
                    self.points.append((pixel, sample_height // 2))
                
            except Exception as ex:
                self.sound_explorer.catch_exception(ex)
                # On error, draw at center line
                self.points.append((pixel, sample_height // 2))
        
        if self.sound_explorer.debug:
            print(f"Number of points: {len(self.points)}")
            if len(self.points) > 0:
                print(f"First few points: {self.points[:5]}")
                print(f"Sample values range: min={min(p[1] for p in self.points)}, max={max(p[1] for p in self.points)}")
                print(f"Max value used for scaling: {max_value}")
        
        self.repaint()
    
    def repaint(self):
        """Repaint the canvas with the waveform."""
        self.canvas.delete("all")
        
        if self.sound_explorer.debug:
            print(f"Repainting canvas with {len(self.points)} points")
        
        # Draw selection if it exists
        if (self.sound_explorer.selection_start != -1 and 
            self.sound_explorer.selection_stop != -1):
            self.canvas.create_rectangle(
                self.sound_explorer.selection_start, 0,
                self.sound_explorer.selection_stop, self.sound_explorer.sample_height,
                fill=self.sound_explorer.SELECTION_COLOR,
                outline=""
            )
        
        # Draw center line first (baseline)
        center_y = self.sound_explorer.sample_height // 2
        self.canvas.create_line(
            0, center_y, self.sound_explorer.sample_width, center_y,
            fill=self.sound_explorer.BAR_COLOR,
            width=1
        )
        
        # Draw waveform lines
        if len(self.points) > 1:
            for i in range(len(self.points) - 1):
                x1, y1 = self.points[i]
                x2, y2 = self.points[i + 1]
                self.canvas.create_line(
                    x1, y1, x2, y2,
                    fill=self.sound_explorer.WAVE_COLOR,
                    width=1
                )
        elif len(self.points) == 1:
            # If only one point, draw a dot
            x, y = self.points[0]
            self.canvas.create_oval(x-1, y-1, x+1, y+1, 
                                  fill=self.sound_explorer.WAVE_COLOR, 
                                  outline=self.sound_explorer.WAVE_COLOR)
        else:
            # No points - draw a message
            self.canvas.create_text(
                self.sound_explorer.sample_width // 2, 
                self.sound_explorer.sample_height // 2,
                text="No waveform data", 
                fill="red", 
                font=("Arial", 12)
            )
            
        # Force canvas update
        self.canvas.update_idletasks()
    
    def update(self):
        """Update the panel display."""
        self.repaint()

class SoundExplorer(MouseMotionListener, ActionListener, MouseListener, LineListener):
    
    
    def __init__(self, sound:Sound):
        """Initialize the SoundExplorer with a sound."""
        # Class constants (equivalent to static final)
        self.ZOOM_IN_HINT = "Click to see all the samples (the number of samples between pixels is 1)"
        self.CURRENT_INDEX_TEXT = "Current Index: "
        self.START_INDEX_TEXT = "Start Index: "
        self.STOP_INDEX_TEXT = "Stop Index: "
        self.SAMPLE_TEXT = "Sample Value: "
    
    # Color constants
        self.SELECTION_COLOR = "grey"
        self.BACKGROUND_COLOR = "black"
        self.WAVE_COLOR = "white"
        self.BAR_COLOR = "cyan"
        
        # Store the primary parameters
        self.sound = sound
        
        # Set up sound explorer relationship
        sound.setSoundExplorer(self)
        
        # Initialize event handling state
        self.mouse_dragged_flag: bool = False
        self.selection_start: int = -1
        self.selection_stop: int = -1
        
        # Initialize sound panel sizing
        self.zoom_out_width: int = 640
        self.zoom_in_width: int = sound.getLengthInFrames()
        self.sample_width: int = self.zoom_out_width
        self.frames_per_pixel: float = sound.getLengthInFrames() / self.sample_width
        self.sample_height: int = 201
        
        # Current pixel position
        self.current_pixel_position: int = 0
        
        # Debug flag
        self.debug: bool = False  # Enable debug for testing
        
        # Main parts of the GUI
        self.sound_frame: Optional[tk.Tk] = None
        self.play_panel: Optional[tk.Frame] = None
        self.scroll_sound: Optional[tk.Frame] = None
        self.sound_panel: Optional[tk.Frame] = None
        
        # Parts of the play panel
        self.start_index_label: Optional[tk.Label] = None
        self.stop_index_label: Optional[tk.Label] = None
        self.button_panel: Optional[tk.Frame] = None
        self.play_entire_button: Optional[tk.Button] = None
        self.play_selection_button: Optional[tk.Button] = None
        self.play_before_button: Optional[tk.Button] = None
        self.play_after_button: Optional[tk.Button] = None
        self.clear_selection_button: Optional[tk.Button] = None
        self.stop_button: Optional[tk.Button] = None
        self.selection_prev_state: bool = False
        
        # Parts of the sound panel
        self.sound_wrapper: Optional[tk.Frame] = None
        self.sample_panel = None  # SamplingPanel equivalent
        
        # Parts of the information panel
        self.info_panel: Optional[tk.Frame] = None
        self.index_label: Optional[tk.Label] = None
        self.num_samples_per_pixel_field: Optional[tk.Entry] = None
        self.index_value: Optional[tk.Entry] = None
        self.sample_label: Optional[tk.Label] = None 
        self.sample_value: Optional[tk.Entry] = None
        self.zoom_button_panel: Optional[tk.Frame] = None
        self.zoom_button: Optional[tk.Button] = None
        self.prev_button: Optional[tk.Button] = None
        self.next_button: Optional[tk.Button] = None
        self.last_button: Optional[tk.Button] = None
        self.first_button: Optional[tk.Button] = None
        
        # Additional sound panel info
        self.sound_panel_height: int = self.sample_height + 20  # Add some padding
        self.base: int = 0  # Equivalent to SimpleSound._SoundIndexOffset
        
        # Event handling info
        self.mouse_pressed_pos: int = 0
        self.mouse_released_pos: int = 0
        self.mouse_pressed_x: int = 0
        self.mouse_released_x: int = 0
        self.start_frame: int = 0
        self.stop_frame: int = 0
        
        # Create the window but don't start mainloop yet
        self.create_window()
        
        # Handle edge case for sounds with less than 640 samples
        if self.frames_per_pixel < 1:
            self.handle_frames_per_pixel(1)
    
    # Interface method implementations
    def mouse_clicked(self, event):
        """Handle mouse click event."""
        self.current_pixel_position = event.x
           
        if self.current_pixel_position == 0:
            self.play_before_button.config(state=tk.DISABLED)
            self.play_after_button.config(state=tk.NORMAL)
        elif self.current_pixel_position < self.sample_width:
            self.play_before_button.config(state=tk.NORMAL)
            self.play_after_button.config(state=tk.NORMAL)
        elif self.current_pixel_position == self.sample_width:
            self.play_before_button.config(state=tk.NORMAL)
            self.play_after_button.config(state=tk.DISABLED)
            
        if self.debug:
            print(f"mouse click: {self.current_pixel_position}")
            
        self.update_index_values()
        self.sample_panel.update()
    
    def mouse_pressed(self, event):
        """Handle mouse press event."""
        self.mouse_pressed_x = event.x
        
    def mouse_released(self, event):
        """Handle mouse release event."""
        self.mouse_released_x = event.x
        
        if self.mouse_dragged_flag:
            self.mouse_pressed_pos = self.mouse_pressed_x
            self.mouse_released_pos = self.mouse_released_x
                
            if self.mouse_pressed_pos > self.mouse_released_pos:  # Selected right to left
                self.mouse_pressed_pos, self.mouse_released_pos = self.mouse_released_pos, self.mouse_pressed_pos
                
            self.start_frame = int(self.mouse_pressed_pos * self.frames_per_pixel)
            self.stop_frame = int(self.mouse_released_pos * self.frames_per_pixel)
                
            # Handle dragging outside the window
            if self.stop_frame >= self.sound.getLengthInFrames():
                self.stop_frame = self.sound.getLengthInFrames()
                
            if self.start_frame < 0:
                self.start_frame = 0
                
            # Update labels
            self.start_index_label.config(text=self.START_INDEX_TEXT + str(self.start_frame))
            self.stop_index_label.config(text=self.STOP_INDEX_TEXT + str(self.stop_frame))
            
            # For highlighting the selection
            self.selection_start = self.mouse_pressed_pos
            self.selection_stop = self.mouse_released_pos
                
            self.sample_panel.update()
            self.play_selection_button.config(state=tk.NORMAL)
            self.clear_selection_button.config(state=tk.NORMAL)
            self.mouse_dragged_flag = False
    
    def mouse_entered(self, event):
        """Handle mouse entered event."""
        pass
        
    def mouse_exited(self, event):
        """Handle mouse exited event."""
        pass
        
    def mouse_dragged(self, event):
        """Handle mouse dragged event."""
        self.mouse_dragged_flag = True
        # Highlight the selection as we drag by simulating mouse release
        self.mouse_released(event)
        
    def mouse_moved(self, event):
        """Handle mouse move event."""
        pass
        
    def update(self, event):
        """Handle line event update."""
        pass
    
    def action_performed(self, event):
        """Handle action events (button clicks, etc.)."""
        pass  # This is handled by action_performed_handler
        
    def action_performed_handler(self, command: str):
        """Handle action events from buttons."""
        try:
            if command == "Play Entire Sound":
                self.sound.play()
            elif command == "Play Selection":
                # Try different method names for playing selection
                if hasattr(self.sound, 'playRange'):
                    self.sound.playRange(1, self.start_frame, self.stop_frame)
                elif hasattr(self.sound, 'play'):
                    # If no range method, just play the whole sound
                    print(f"Playing selection from {self.start_frame} to {self.stop_frame}")
                    self.sound.play()
            elif command == "Stop":
                # Try different methods to stop playback
                if hasattr(self.sound, 'stop'):
                    self.sound.stop()
                elif hasattr(self.sound, 'stopPlaying'):
                    self.sound.stopPlaying()
                else:
                    print("Stop not implemented")
            elif command == "Zoom In":
                self.handle_zoom_in(True)
            elif command == "Zoom Out":
                self.handle_zoom_out()
            elif command == "Play Before":
                # Try different method names
                if hasattr(self.sound, 'playRange'):
                    self.sound.playRange(1, 0, int(self.current_pixel_position * self.frames_per_pixel))
                elif hasattr(self.sound, 'PlayRange'):
                    self.sound.PlayRange(1, 0, int(self.current_pixel_position * self.frames_per_pixel))
                else:
                    print(f"Playing before position {self.current_pixel_position}")
                    self.sound.play()
            elif command == "Play After":
                # Try different method names
                if hasattr(self.sound, 'playRange'):
                    self.sound.playRange(1, int(self.current_pixel_position * self.frames_per_pixel), self.sound.getLengthInFrames() - 1)
                elif hasattr(self.sound, 'PlayRange'):
                    self.sound.PlayRange(1, int(self.current_pixel_position * self.frames_per_pixel), self.sound.getLengthInFrames() - 1)
                else:
                    print(f"Playing after position {self.current_pixel_position}")
                    self.sound.play()
        except Exception as ex:
            self.catch_exception(ex)
    
    def handle_zoom_in(self, from_button: bool):
        """Handle zoom in functionality."""
        if self.frames_per_pixel > 1:
            self.frames_per_pixel = max(1, self.frames_per_pixel // 2)
            self.sample_width = int(self.sound.getLengthInFrames() / self.frames_per_pixel)
            
            # Update display
            self._update_panel_sizes()
            self.sample_panel.create_wave_form()
            self.update_index_values()
            self.sample_panel.update()
            
            if self.frames_per_pixel == 1:
                self.zoom_button.config(text="Zoom Out")
    
    def handle_zoom_out(self):
        """Handle zoom out - simplified."""
        self.zoom_button.config(text="Zoom Out")
        
        self.sample_width = self.zoom_out_width
        self.frames_per_pixel = self.sound.getLengthInFrames() / self.sample_width
        
        if self.debug:
            print(f"Zoom Out: currentPixelPosition = {self.current_pixel_position}")
        
        # Update panel sizes and recreate waveform
        self._update_panel_sizes()
        self.sample_panel.create_wave_form()
        
        self.update_index_values()
        self.sample_panel.update()
    
    def check_scroll(self):
        """Check that the current position is in the viewing area and scroll if needed."""
        # Only do this if we are not zoomed out
        if self.sample_width != self.zoom_out_width:
            # This would implement scrolling logic for tkinter
            # More complex implementation needed for proper scrolling
            pass
    
    def handle_zoom_in_index(self, index: int):
        """Handle zoom in to view all sample values at specific index."""
        if index % self.frames_per_pixel != 0:
            # Do normal zoom in on current position
            self.handle_zoom_in(False)
            
        # Change current position to the passed index
        self.current_pixel_position = int(index / self.frames_per_pixel) - self.base
            
        # Check scroll and repaint
        self.check_scroll()
        self.sample_panel.update()
    
    def create_window(self):
        """Create and display the main window and all GUI components."""
        # Get filename for window title
        file_name = self.sound.getFileName()
        if file_name is None:
            file_name = "no file name"
        
        # Create main window
        self.sound_frame = tk.Tk()
        self.sound_frame.title(file_name)
        
        # Set up window properties
        self.sound_frame.protocol("WM_DELETE_WINDOW", self._on_window_close)
        
        # Create the play panel (top)
        self.create_play_panel()
        self.play_panel.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # Create the sound panel (center)
        self.create_sound_panel()
        self.sound_panel.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create the info panel (bottom)
        self.create_info_panel()
        self.info_panel.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        # Configure window final properties
        self.sound_frame.update_idletasks()  # Calculate required size
        
        # Set a reasonable window size
        window_width = max(self.sample_width + 20, 800)
        window_height = self.sample_height + 200  # Extra space for controls
        self.sound_frame.geometry(f"{window_width}x{window_height}")
        
        # Make window appear in front
        self.sound_frame.lift()
        self.sound_frame.attributes('-topmost', True)
        self.sound_frame.after_idle(lambda: self.sound_frame.attributes('-topmost', False))
        self.sound_frame.focus_force()
        
        # Make window visible but don't start mainloop here
        self.sound_frame.deiconify()
    
    def show(self):
        """Show the window and start the event loop. Call this after creating the SoundExplorer."""
        if self.sound_frame:
            try:
                self.sound_frame.mainloop()
            except KeyboardInterrupt:
                print("Interrupted by user")
            except Exception as e:
                print(f"Mainloop error: {e}")
            finally:
                # Clean up
                try:
                    if self.sound_frame and self.sound_frame.winfo_exists():
                        self.sound_frame.destroy()
                except:
                    pass
    
    def run(self):
        """Alias for show() method."""
        self.show()
    
    def _on_window_close(self):
        """Handle window close event."""
        # Try to stop any playing sounds
        try:
            if hasattr(self.sound, 'stop'):
                self.sound.stop()
            elif hasattr(self.sound, 'stopPlaying'):
                self.sound.stopPlaying()
        except:
            pass
        
        # Don't destroy the window immediately, just withdraw it
        if self.sound_frame:
            self.sound_frame.withdraw()
            # Use after_idle to destroy later, preventing immediate exit
            self.sound_frame.after_idle(self.sound_frame.quit)
    
    def close(self):
        """Programmatically close the window."""
        self._on_window_close()
    
    def is_visible(self):
        """Check if the window is currently visible."""
        if self.sound_frame:
            try:
                return self.sound_frame.winfo_viewable()
            except:
                return False
        return False
    
    def create_play_panel(self):
        """Create the panel containing play controls."""
        # Set up the play panel
        self.play_panel = tk.Frame(self.sound_frame)
        
        # Create the selection panel items
        selection_panel = tk.Frame(self.play_panel)
        self.start_index_label = tk.Label(selection_panel, text=self.START_INDEX_TEXT + "N/A")
        self.stop_index_label = tk.Label(selection_panel, text=self.STOP_INDEX_TEXT + "N/A")
        self.play_selection_button = self.make_button("Play Selection", False, selection_panel)
        self.clear_selection_button = self.make_button("Clear Selection", False, selection_panel)
        
        self.start_index_label.pack(side=tk.LEFT, padx=5)
        self.stop_index_label.pack(side=tk.LEFT, padx=5)
        
        # Set up the button panel
        self.button_panel = tk.Frame(self.play_panel)
        self.play_entire_button = self.make_button("Play Entire Sound", True, self.button_panel)
        self.selection_prev_state = False
        self.play_before_button = self.make_button("Play Before", False, self.button_panel)
        self.play_after_button = self.make_button("Play After", True, self.button_panel)
        self.stop_button = self.make_button("Stop", True, self.button_panel)
        
        # Pack panels
        self.button_panel.pack(side=tk.TOP, fill=tk.X)
        selection_panel.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_sound_panel(self):
        """Create the panel that displays the sound waveform."""
        self.sound_panel = tk.Frame(self.sound_frame, relief=tk.SUNKEN, bd=2)
        
        # Single sound wrapper and panel
        self.sound_wrapper = tk.Frame(self.sound_panel)
        self.sample_panel = SamplingPanel(self.sound_wrapper, self)
        
        self.sample_panel.pack()
        self.sound_wrapper.pack(fill=tk.BOTH, expand=True)
    
    def create_info_panel(self):
        """Create the panel showing current index and sample values."""
        # Create the information panel
        self.info_panel = tk.Frame(self.sound_frame)
        
        # Create the index panel
        index_panel = tk.Frame(self.info_panel)
        self.setup_index_panel(index_panel)
        
        # Create zoom panel with zoom button
        self.zoom_button_panel = tk.Frame(self.info_panel)
        self.zoom_button = self.make_button("Zoom In", True, self.zoom_button_panel)
        
        index_panel.pack(side=tk.TOP, fill=tk.X)
        self.zoom_button_panel.pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_index_panel(self, index_panel: tk.Frame):
        """Set up the index panel with navigation buttons and value displays."""
        top_panel = tk.Frame(index_panel)
        
        # Create navigation buttons
        self.first_button = tk.Button(top_panel, text="<<", command=self._first_clicked)
        self.prev_button = tk.Button(top_panel, text="<", command=self._prev_clicked)
        self.next_button = tk.Button(top_panel, text=">", command=self._next_clicked)
        self.last_button = tk.Button(top_panel, text=">>", command=self._last_clicked)
        
        # Create value fields - simplified
        self.index_value = tk.Entry(top_panel, width=10)
        self.index_value.insert(0, str(self.base))
        self.index_value.bind('<Return>', self._index_value_changed)
        
        self.sample_value = tk.Entry(top_panel, width=10, state='readonly')
        
        # Create labels - simplified
        self.index_label = tk.Label(top_panel, text=self.CURRENT_INDEX_TEXT)
        self.sample_label = tk.Label(top_panel, text=self.SAMPLE_TEXT)
        
        self.update_index_values()
        
        # Pack widgets - much simpler layout
        self.first_button.pack(side=tk.LEFT, padx=2)
        self.prev_button.pack(side=tk.LEFT, padx=2)
        self.index_label.pack(side=tk.LEFT, padx=5)
        self.index_value.pack(side=tk.LEFT, padx=2)
        self.sample_label.pack(side=tk.LEFT, padx=5)
        self.sample_value.pack(side=tk.LEFT, padx=2)
        self.next_button.pack(side=tk.LEFT, padx=2)
        self.last_button.pack(side=tk.LEFT, padx=2)
        
        # Bottom panel for frames per pixel
        bottom_panel = tk.Frame(index_panel)
        frames_label = tk.Label(bottom_panel, text="Samples between pixels: ")
        self.num_samples_per_pixel_field = tk.Entry(bottom_panel, width=10)
        self.num_samples_per_pixel_field.insert(0, str(int(self.frames_per_pixel)))
        self.num_samples_per_pixel_field.bind('<Return>', self._frames_per_pixel_changed)
        
        frames_label.pack(side=tk.LEFT)
        self.num_samples_per_pixel_field.pack(side=tk.LEFT)
        
        # Pack panels
        top_panel.pack(side=tk.TOP, pady=2)
        bottom_panel.pack(side=tk.BOTTOM, pady=2)
        index_panel.pack(fill=tk.X)
    
    def make_button(self, name: str, enabled: bool, panel: tk.Frame) -> tk.Button:
        """Method to create a button and add it to the passed panel."""
        button = tk.Button(panel, text=name, state=tk.NORMAL if enabled else tk.DISABLED)
        button.bind('<Button-1>', self._button_clicked)
        button.pack(side=tk.LEFT, padx=2)
        return button
    
    def clear_selection(self):
        """Method to clear the selection information."""
        self.selection_start = -1
        self.selection_stop = -1
        self.start_index_label.config(text=self.START_INDEX_TEXT + "N/A")
        self.stop_index_label.config(text=self.STOP_INDEX_TEXT + "N/A")
        self.sample_panel.update()
        self.play_selection_button.config(state=tk.DISABLED)
        self.clear_selection_button.config(state=tk.DISABLED)
    
    def update_index_values(self):
        """Method to update the index values to the current index position."""
        cur_frame = int(self.current_pixel_position * self.frames_per_pixel) + self.base
        
        # Update the display of the current sample (frame) index
        self.index_value.delete(0, tk.END)
        self.index_value.insert(0, str(cur_frame))
        
        # Update the number of samples per (between) pixels field
        if self.num_samples_per_pixel_field is not None:
            self.num_samples_per_pixel_field.delete(0, tk.END)
            self.num_samples_per_pixel_field.insert(0, str(int(self.frames_per_pixel)))
        
        # Try to update the value at the current sample index
        try:
            sample = self.sound.getSample(cur_frame - self.base)
            self.sample_value.config(state='normal')
            self.sample_value.delete(0, tk.END)
            self.sample_value.insert(0, f"{sample:.4f}")
            self.sample_value.config(state='readonly')
        except Exception as ex:
            self.catch_exception(ex)
    
    def handle_frames_per_pixel(self, num_frames: int):
        """Handle setting desired number of frames per pixel - simplified."""
        # Get current index from pixel position and frames per pixel
        curr_index = int(self.current_pixel_position * self.frames_per_pixel)
        self.sample_width = max(1, self.sound.getLengthInFrames() // num_frames)
        self.frames_per_pixel = num_frames
        
        if self.sample_width > 0:
            self.current_pixel_position = max(0, int(curr_index / self.frames_per_pixel))
        
        # Update panel sizes and recreate waveform
        self._update_panel_sizes()
        self.sample_panel.create_wave_form()
        
        # Update display
        self.update_index_values()
        self.check_scroll()
        self.sample_panel.update()
    
    def _update_panel_sizes(self):
        """Update all panel sizes based on current sample width."""
        # Update sound panel
        self.sound_panel.config(width=self.sample_width + 10, height=self.sound_panel_height)
        
        # Update wrapper and sample panel
        self.sound_wrapper.config(width=self.sample_width)
        self.sample_panel.config(width=self.sample_width, height=self.sample_height)
        
        # Update canvas size
        self.sample_panel.canvas.config(width=self.sample_width, height=self.sample_height)

    def set_base(self, base: int):
        """Method to set the base for the index."""
        self.base = base
    
    def catch_exception(self, ex: Exception):
        """Handle exceptions that occur during sound processing."""
        if self.debug:
            print(f"Exception caught: {ex}")
    
    def debug_sound_methods(self):
        """Debug helper to see what methods are available on the sound object."""
        print("Available methods on sound object:")
        methods = [method for method in dir(self.sound) if not method.startswith('_')]
        for method in sorted(methods):
            print(f"  - {method}")
        
        # Test some basic properties
        print(f"\nSound properties:")
        try:
            print(f"  - Length in frames: {self.sound.getLengthInFrames()}")
        except:
            print("  - getLengthInFrames() failed")
            
        try:
            print(f"  - Number of samples: {self.sound.getNumSamples()}")
        except:
            print("  - getNumSamples() failed")
            
        try:
            print(f"  - Sample at index 0: {self.sound.getSample(0)}")
            print(f"  - Sample at index 100: {self.sound.getSample(100)}")
        except Exception as e:
            print(f"  - getSample() failed: {e}")
            
        return methods
    
    def _button_clicked(self, event):
        """Handle button click events."""
        button = event.widget
        command = button.cget('text')
        
        if command == "Clear Selection":
            self.clear_selection()
        else:
            self.action_performed_handler(command)
    
    def _first_clicked(self):
        """Handle first button press."""
        self.current_pixel_position = 0
        self.update_index_values()
        self.check_scroll()
        self.sample_panel.update()
    
    def _prev_clicked(self):
        """Handle previous button press."""
        self.current_pixel_position = max(0, self.current_pixel_position - 1)
        self.update_index_values()
        self.check_scroll()
        self.sample_panel.update()
    
    def _next_clicked(self):
        """Handle next button press."""
        max_pos = int((self.sound.getNumSamples() - 1) / self.frames_per_pixel)
        self.current_pixel_position = min(max_pos, self.current_pixel_position + 1)
        self.update_index_values()
        self.check_scroll()
        self.sample_panel.update()
    
    def _last_clicked(self):
        """Handle last button press."""
        self.current_pixel_position = int((self.sound.getNumSamples() - 1) / self.frames_per_pixel)
        self.update_index_values()
        self.check_scroll()
        self.sample_panel.update()
    
    def _index_value_changed(self, event):
        """Handle index value text field change."""
        try:
            index = int(self.index_value.get())
            self.handle_zoom_in_index(index)
            self.update_index_values()
        except ValueError:
            pass  # Invalid input, ignore
    
    def _frames_per_pixel_changed(self, event):
        """Handle frames per pixel text field change."""
        try:
            frames = int(self.num_samples_per_pixel_field.get())
            if frames > 0:
                self.handle_frames_per_pixel(frames)
                self.update_index_values()
        except ValueError:
            pass  # Invalid input, ignore