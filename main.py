import json
import tkinter as tk
from pynput import keyboard
import mpv
from threading import Timer

# Load JSON file
with open('urls.json', 'r') as file:
    data = json.load(file)

# Extract URLs
urls = data['urls']

# Initialize MPV player
player = mpv.MPV(
    ytdl=True,
    fullscreen=True,
    input_default_bindings=False,
    user_agent="Mozilla/5.0"
)

# Variables to store the current channel index, input buffer, and timer
current_index = -1
input_buffer = ""
timer = None
playback_time_printed = False

# Create a tkinter window
number_window = tk.Tk()
number_window.attributes("-topmost", True)
number_window.overrideredirect(True)  # Remove window decorations

# Get the screen width and height
screen_width = number_window.winfo_screenwidth()
screen_height = number_window.winfo_screenheight()

# Create the loading window
loading_window = tk.Toplevel(number_window)
loading_window.attributes("-topmost", True)
loading_window.overrideredirect(True)  # Remove window decorations
loading_label = tk.Label(loading_window, text="Loading", font=("Helvetica", 77, "bold"), fg="white", bg="#1B1212")
loading_label.pack(expand=True)

# Position the loading window at the center of the screen
loading_window.geometry(f"+{screen_width//2 - 50}+{screen_height//2 - 20}")

# Hide the loading window initially
loading_window.withdraw()

# Define the loading animation
loading_animations = ['.', '..', '...', '....']
loading_index = 0

# Function to update the loading animation
def update_loading_animation():
    global loading_index
    loading_label.config(text=loading_animations[loading_index])
    loading_index = (loading_index + 1) % len(loading_animations)
    loading_window.after(250, update_loading_animation)  # Update every 0.25 seconds

# Start the loading animation
update_loading_animation()

# Calculate the desired width and height of the main window (e.g., 10% of the screen width)
window_width = int(screen_width * 0.13)
window_height = int(screen_width * 0.13)

# Calculate the position of the main window
window_x = int(screen_width * 0.05)
window_y = int(screen_height * 0.05)

# Set the geometry of the main window
number_window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

# Change background color to black
number_window.config(bg="#1B1212")

# Label to display the pressed keys
label = tk.Label(number_window, text="", font=("Helvetica", 134, "bold"), fg="white", bg="#1B1212")
label.pack(expand=True, pady=(20, 0))

# Hide the main window initially
number_window.withdraw()

# Function to handle 'playback-time' changes
def handle_playback_time(name, value):
    global playback_time_printed
    if value is not None and value > 0.0 and not playback_time_printed:
        print(f"playback-time: {value}")
        loading_window.withdraw()  # Hide the loading window
        playback_time_printed = True

# Bind the 'playback-time' property to the handler
player.observe_property("playback-time", handle_playback_time)

def play_url(index):
    global player, playback_time_printed
    url = urls[index]['url']
    print(f"Playing {urls[index]['name']} - {url}")
    loading_window.deiconify()  # Show the loading window
    playback_time_printed = False  # Reset the flag whenever a new URL is played
    player.play(url)

def reset_input_buffer():
    global input_buffer, timer
    if input_buffer:
        index = int(input_buffer)
        if 0 <= index < len(urls):
            print(f"Key {index} pressed")
            label.config(text=input_buffer)
            play_url(index)
        input_buffer = ""
    if timer:
        timer.cancel()
        timer = None
    label.config(text="")
    number_window.withdraw()  # Hide the main window

def on_press(key):
    global current_index, input_buffer, timer
    try:
        if key.char.isdigit():
            if len(input_buffer) < 2:  # Only update buffer if it's less than 2 digits
                if timer:
                    timer.cancel()
                input_buffer += key.char
                label.config(text=input_buffer)
                number_window.deiconify()  # Show the main window
                number_window.update_idletasks()  # Ensure the window is updated
                timer = Timer(3.0, reset_input_buffer)
                timer.start()
    except AttributeError:
        # Handle special keys (e.g., function keys)
        pass

# Create a listener for key press events
listener = keyboard.Listener(on_press=on_press)

# Start the listener
listener.start()

# Keep the program running
print("Press keys 0-9 to switch channels. Press 'esc' to exit.")

# Wait for the 'esc' key to exit
def on_press_exit(key):
    if key == keyboard.Key.esc:
        listener.stop()
        number_window.quit()
        return False

with keyboard.Listener(on_press=on_press_exit) as exit_listener:
    number_window.mainloop()
    exit_listener
