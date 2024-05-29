import tkinter as tk
import config

class GUIManager:
    def __init__(self, player):
        self.player = player
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the root window

        self.number_window = tk.Toplevel(self.root)
        self.number_window.attributes("-topmost", True)
        self.number_window.overrideredirect(True)

        screen_width = self.number_window.winfo_screenwidth()
        screen_height = self.number_window.winfo_screenheight()

        self.loading_window = tk.Toplevel(self.root)
        self.loading_window.attributes("-topmost", True)
        self.loading_window.overrideredirect(True)
        self.loading_label = tk.Label(self.loading_window, text="Loading", font=config.LOADING_FONT, fg=config.TEXT_COLOR, bg=config.BG_COLOR)
        self.loading_label.pack(expand=True)
        self.loading_window.geometry(f"+{screen_width//2 - 50}+{screen_height//2 - 20}")
        self.loading_window.withdraw()

        self.channel_info_window = tk.Toplevel(self.root)
        self.channel_info_window.attributes("-topmost", True)
        self.channel_info_window.overrideredirect(True)
        self.channel_info_label = tk.Label(self.channel_info_window, text="", font=config.CHANNEL_INFO_FONT, fg=config.TEXT_COLOR, bg=config.BG_COLOR)
        self.channel_info_label.pack(expand=True)
        self.channel_info_window.geometry(f"+0+{screen_height - 100}")
        self.channel_info_window.withdraw()

        self.loading_animations = config.LOADING_ANIMATIONS
        self.loading_index = 0

        window_width = int(screen_width * config.WINDOW_WIDTH_RATIO)
        window_height = int(screen_width * config.WINDOW_HEIGHT_RATIO)
        window_x = int(screen_width * config.WINDOW_X_RATIO)
        window_y = int(screen_height * config.WINDOW_Y_RATIO)

        self.number_window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")
        self.number_window.config(bg=config.BG_COLOR)

        self.label = tk.Label(self.number_window, text="", font=config.NUMBER_FONT, fg=config.TEXT_COLOR, bg=config.BG_COLOR)
        self.label.pack(expand=True, pady=(20, 0))

        self.number_window.withdraw()

        self.update_loading_animation()

    def update_loading_animation(self):
        self.loading_label.config(text=self.loading_animations[self.loading_index])
        self.loading_index = (self.loading_index + 1) % len(self.loading_animations)
        self.loading_window.after(config.LOADING_UPDATE_INTERVAL, self.update_loading_animation)

    def show_loading(self):
        self.loading_window.deiconify()

    def hide_loading(self):
        self.loading_window.withdraw()

    def show_channel_info(self, index, name):
        self.channel_info_label.config(text=f"Channel {index}: {name}")
        self.channel_info_window.deiconify()
        self.channel_info_window.after(config.CHANNEL_INFO_DISPLAY_DURATION, self.hide_channel_info)

    def hide_channel_info(self):
        self.channel_info_window.withdraw()

    def show_number_window(self):
        self.number_window.deiconify()
        self.number_window.update_idletasks()

    def hide_number_window(self):
        self.number_window.withdraw()

    def update_number_window_label(self, text):
        self.label.config(text=text)
