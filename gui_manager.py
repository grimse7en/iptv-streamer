import tkinter as tk
import config

class GUIManager:
    def __init__(self):
        # Initialize the root window
        self.root = tk.Tk()
        self.root.withdraw()
        
        # Define all instance attributes
        self.number_window = None
        self.loading_window = None
        self.channel_info_window = None
        self.label = None
        self.loading_label = None
        self.channel_info_label = None
        self.loading_animations = config.LOADING_ANIMATIONS
        self.loading_index = 0

        # Set up the windows
        self.setup_windows()

    def setup_windows(self):
        """Sets up all the application windows."""
        self.setup_number_window()
        self.setup_loading_window()
        self.setup_channel_info_window()
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

        screen_width = self.channel_info_window.winfo_screenwidth()
        screen_height = self.channel_info_window.winfo_screenheight()
        channel_info_x_ratio = 0.05
        channel_info_y_ratio = 0.9
        self.channel_info_window.geometry(f"+{int(screen_width * channel_info_x_ratio)}+{int(screen_height * channel_info_y_ratio)}")

        self.channel_info_label = tk.Label(self.channel_info_window, text="", font=config.CHANNEL_INFO_FONT, fg=config.TEXT_COLOR, bg=config.BG_COLOR)
        self.channel_info_label.pack(expand=True)
        self.channel_info_window.withdraw()

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
        self.channel_info_label.config(text=f"Channel {index}: {name}")
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

    def run(self):
        """Runs the Tkinter main loop."""
        self.root.mainloop()
