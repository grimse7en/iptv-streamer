import tkinter as tk
import config

class GUIManager:
    @staticmethod
    def initialize(player):
        GUIManager.player = player
        GUIManager.root = tk.Tk()
        GUIManager.root.withdraw()  # Hide the root window

        GUIManager.number_window = tk.Toplevel(GUIManager.root)
        GUIManager.number_window.attributes("-topmost", True)
        GUIManager.number_window.overrideredirect(True)

        screen_width = GUIManager.number_window.winfo_screenwidth()
        screen_height = GUIManager.number_window.winfo_screenheight()

        GUIManager.loading_window = tk.Toplevel(GUIManager.root)
        GUIManager.loading_window.attributes("-topmost", True)
        GUIManager.loading_window.overrideredirect(True)
        GUIManager.loading_label = tk.Label(GUIManager.loading_window, text="Loading", font=config.LOADING_FONT, fg=config.TEXT_COLOR, bg=config.BG_COLOR)
        GUIManager.loading_label.pack(expand=True)
        GUIManager.loading_window.geometry(f"+{screen_width//2 - 50}+{screen_height//2 - 20}")
        GUIManager.loading_window.withdraw()

        GUIManager.channel_info_window = tk.Toplevel(GUIManager.root)
        GUIManager.channel_info_window.attributes("-topmost", True)
        GUIManager.channel_info_window.overrideredirect(True)
        GUIManager.channel_info_label = tk.Label(GUIManager.channel_info_window, text="", font=config.CHANNEL_INFO_FONT, fg=config.TEXT_COLOR, bg=config.BG_COLOR)
        GUIManager.channel_info_label.pack(expand=True)
        GUIManager.channel_info_window.geometry(f"+0+{screen_height - 100}")
        GUIManager.channel_info_window.withdraw()

        GUIManager.loading_animations = config.LOADING_ANIMATIONS
        GUIManager.loading_index = 0

        window_width = int(screen_width * config.WINDOW_WIDTH_RATIO)
        window_height = int(screen_width * config.WINDOW_HEIGHT_RATIO)
        window_x = int(screen_width * config.WINDOW_X_RATIO)
        window_y = int(screen_height * config.WINDOW_Y_RATIO)

        GUIManager.number_window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")
        GUIManager.number_window.config(bg=config.BG_COLOR)

        GUIManager.label = tk.Label(GUIManager.number_window, text="", font=config.NUMBER_FONT, fg=config.TEXT_COLOR, bg=config.BG_COLOR)
        GUIManager.label.pack(expand=True, pady=(20, 0))

        GUIManager.number_window.withdraw()

        GUIManager.update_loading_animation()

    @staticmethod
    def update_loading_animation():
        GUIManager.loading_label.config(text=GUIManager.loading_animations[GUIManager.loading_index])
        GUIManager.loading_index = (GUIManager.loading_index + 1) % len(GUIManager.loading_animations)
        GUIManager.loading_window.after(config.LOADING_UPDATE_INTERVAL, GUIManager.update_loading_animation)

    @staticmethod
    def show_loading():
        GUIManager.loading_window.deiconify()

    @staticmethod
    def hide_loading():
        GUIManager.loading_window.withdraw()

    @staticmethod
    def show_channel_info(index, name):
        GUIManager.channel_info_label.config(text=f"Channel {index}: {name}")
        GUIManager.channel_info_window.deiconify()
        GUIManager.channel_info_window.after(config.CHANNEL_INFO_DISPLAY_DURATION, GUIManager.hide_channel_info)

    @staticmethod
    def hide_channel_info():
        GUIManager.channel_info_window.withdraw()

    @staticmethod
    def show_number_window():
        GUIManager.number_window.deiconify()
        GUIManager.number_window.update_idletasks()

    @staticmethod
    def hide_number_window():
        GUIManager.number_window.withdraw()

    @staticmethod
    def update_label(text):
        GUIManager.label.config(text=text)
