import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import config
import os

class GUIManager:
    def __init__(self):
        # Initialize the root window
        self.root = tk.Tk()
        self.root.withdraw()
        
        # Define all instance attributes
        self.number_window = None
        self.loading_window = None
        self.channel_info_window = None
        self.message_window = None
        self.fullscreen_window = None
        self.label = None
        self.loading_label = None
        self.channel_info_label = None
        self.message_label = None
        self.loading_animations = config.LOADING_ANIMATIONS
        self.loading_index = 0

        # Set up the windows
        self.setup_windows()

    def setup_windows(self):
        """Sets up all the application windows."""
        self.setup_number_window()
        self.setup_loading_window()
        self.setup_channel_info_window()
        self.setup_message_window()
        self.update_loading_animation()

    def setup_number_window(self):
        """Sets up the number display window."""
        self.number_window = tk.Toplevel(self.root)
        self.number_window.attributes("-topmost", True)
        self.number_window.overrideredirect(True)

        screen_width = self.number_window.winfo_screenwidth()
        screen_height = self.number_window.winfo_screenheight()
        window_width = int(screen_width * config.WINDOW_WIDTH_RATIO)
        window_height = int(screen_width * config.WINDOW_HEIGHT_RATIO)
        window_x = int(screen_width * config.WINDOW_X_RATIO)
        window_y = int(screen_height * config.WINDOW_Y_RATIO)
        self.number_window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")
        self.number_window.config(bg=config.BG_COLOR)

        self.label = tk.Label(self.number_window, text="", font=config.NUMBER_FONT, fg=config.TEXT_COLOR, bg=config.BG_COLOR)
        self.label.pack(expand=True, pady=(20, 0))
        self.number_window.withdraw()

    def setup_loading_window(self):
        """Sets up the loading animation window."""
        self.loading_window = tk.Toplevel(self.root)
        self.loading_window.attributes("-topmost", True)
        self.loading_window.overrideredirect(True)

        screen_width = self.loading_window.winfo_screenwidth()
        screen_height = self.loading_window.winfo_screenheight()
        self.loading_window.geometry(f"+{screen_width//2 - 50}+{screen_height//2 - 20}")

        self.loading_label = tk.Label(self.loading_window, text="Loading", font=config.LOADING_FONT, fg=config.TEXT_COLOR, bg=config.BG_COLOR)
        self.loading_label.pack(expand=True)
        self.loading_window.withdraw()

    def setup_channel_info_window(self):
        """Sets up the channel information display window."""
        self.channel_info_window = tk.Toplevel(self.root)
        self.channel_info_window.attributes("-topmost", True)
        self.channel_info_window.overrideredirect(True)
        self.channel_info_window.configure(bg=config.BG_COLOR)

        screen_width = self.channel_info_window.winfo_screenwidth()
        screen_height = self.channel_info_window.winfo_screenheight()
        channel_info_x_ratio = 0.05
        channel_info_y_ratio = 0.9
        self.channel_info_window.geometry(f"+{int(screen_width * channel_info_x_ratio)}+{int(screen_height * channel_info_y_ratio)}")

        self.channel_info_label = tk.Label(self.channel_info_window, text="", font=config.CHANNEL_INFO_FONT, fg=config.TEXT_COLOR, bg=config.BG_COLOR)
        self.channel_info_label.pack(expand=True, padx=20, pady=15)
        self.channel_info_window.withdraw()

    def setup_message_window(self):
        """Sets up the message display window."""
        self.message_window = tk.Toplevel(self.root)
        self.message_window.attributes("-topmost", True)
        self.message_window.overrideredirect(True)
        self.message_window.configure(bg=config.BG_COLOR)

        screen_width = self.loading_window.winfo_screenwidth()
        screen_height = self.loading_window.winfo_screenheight()
        self.message_window.geometry(f"+{screen_width//2 - 270}+{screen_height//2 + 100}")

        self.message_label = tk.Label(self.message_window, text="", font=config.MESSAGE_WINDOW_FONT, fg=config.TEXT_COLOR, bg=config.BG_COLOR)
        self.message_label.pack(expand=True, padx=20, pady=15)
        self.message_window.withdraw()

    def setup_fullscreen_window(self, items):
        """Sets up the fullscreen window with a grid layout based on the items."""
        self.fullscreen_window = tk.Toplevel(self.root)
        self.fullscreen_window.attributes("-fullscreen", True)
        self.fullscreen_window.config(bg=config.GRID_BG_COLOR)

        # Hide the cursor
        self.fullscreen_window.config(cursor="none")

        # Filter out the item with index 0
        items = [item for item in items if item['index'] != 0]

        # Calculate the number of rows and columns needed
        num_items = len(items)
        columns = int(num_items**0.5)
        rows = (num_items // columns) + (1 if num_items % columns != 0 else 0)

        # Define maximum size for the images
        max_width = 600
        max_height = 600

        # Set the fixed size for each grid cell
        cell_width = 600
        cell_height = 600

        # Create a grid layout
        for r in range(rows):
            self.fullscreen_window.grid_rowconfigure(r, weight=1)
            for c in range(columns):
                self.fullscreen_window.grid_columnconfigure(c, weight=1)
                index = r * columns + c
                if index < num_items:
                    item = items[index]
                    # Use the item's color or default to GRID_BG_COLOR if not specified
                    bg_color = item.get('colour', config.GRID_BG_COLOR)
                    frame = tk.Frame(self.fullscreen_window, width=cell_width, height=cell_height, bg=bg_color, bd=2, relief="solid")
                    frame.grid(row=r, column=c, sticky="nsew", padx=11, pady=11)
                    frame.grid_propagate(False)  # Prevent frame from resizing to fit content

                    # Load and resize the image while maintaining aspect ratio
                    img_path = os.path.join("img", f"{item['index']}.png")
                    if os.path.exists(img_path):
                        img = Image.open(img_path)
                        img.thumbnail((max_width, max_height), Image.LANCZOS)
                        img = ImageTk.PhotoImage(img)
                    else:
                        img = None  # Placeholder for no image

                    # Display the index in the middle of the height
                    index_label = tk.Label(frame, text=f"{item['index']}", font=config.GRID_FONT, fg=config.TEXT_COLOR, bg=bg_color)
                    index_label.place(relx=0.05, rely=0.5, anchor="w")  # Center vertically, left align horizontally

                    # Display the image
                    if img:
                        image_label = tk.Label(frame, image=img, bg=bg_color)
                        image_label.image = img  # Keep a reference to avoid garbage collection
                        image_label.place(relx=0.6, rely=0.5, anchor="center")  # Center the image in the frame
                    else:
                        image_label = tk.Label(frame, text="", bg=bg_color)
                        image_label.place(relx=0.6, rely=0.5, anchor="center")  # Center the placeholder label

                    # Display the name
                    #name_label = tk.Label(frame, text=item['name'], font=config.GRID_FONT, fg=config.TEXT_COLOR, bg=bg_color)
                    #name_label.grid(row=1, column=1, sticky="nw")

        self.fullscreen_window.withdraw()

    def show_fullscreen_window(self):
        """Shows the fullscreen window with the provided items."""
        self.fullscreen_window.deiconify()

    def hide_fullscreen_window(self):
        """Hides the fullscreen window."""
        self.fullscreen_window.withdraw()

    def update_loading_animation(self):
        """Updates the loading animation."""
        self.loading_label.config(text=self.loading_animations[self.loading_index])
        self.loading_index = (self.loading_index + 1) % len(self.loading_animations)
        self.loading_window.after(config.LOADING_UPDATE_INTERVAL, self.update_loading_animation)

    def show_loading(self):
        """Shows the loading window."""
        self.loading_window.deiconify()

    def hide_loading(self):
        """Hides the loading window."""
        self.loading_window.withdraw()

    def show_channel_info(self, index, name):
        """Shows the channel information window."""
        self.channel_info_label.config(text=f"{index}.   {name}")
        self.channel_info_window.deiconify()
        self.channel_info_window.after(config.CHANNEL_INFO_DISPLAY_DURATION, self.hide_channel_info)

    def hide_channel_info(self):
        """Hides the channel information window."""
        self.channel_info_window.withdraw()

    def show_number_window(self):
        """Shows the number display window."""
        self.number_window.deiconify()
        self.number_window.update_idletasks()

    def hide_number_window(self):
        """Hides the number display window."""
        self.number_window.withdraw()

    def update_number_window_label(self, text):
        """Updates the label in the number display window."""
        self.label.config(text=text)

    def show_message_window(self, message):
        """Shows the message window with the provided message."""
        self.message_label.config(text=message)
        self.message_window.deiconify()

    def hide_message_window(self):
        """Hides the message window."""
        self.message_window.withdraw()

    def run(self):
        """Runs the Tkinter main loop."""
        self.root.mainloop()
