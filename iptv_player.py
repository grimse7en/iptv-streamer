import mpv
from threading import Timer
import config

class IPTVPlayer:
    def __init__(self, channels, gui_manager):
        self.channels = channels
        self.gui_manager = gui_manager
        self.current_channel_index = config.DEFAULT_CHANNEL_INDEX
        self.input_buffer = ""
        self.timer = None
        self.playback_time_printed = False

        self.mpv = mpv.MPV(
            ytdl=True,
            fullscreen=True,
            input_default_bindings=False,
            user_agent="Mozilla/5.0"
        )
        
        self.mpv.observe_property("playback-time", self.handle_playback_time)
        self.play_channel(self.current_channel_index)

    def handle_playback_time(self, name, value):
        if value is not None and value > 0.0 and not self.playback_time_printed:
            print(f"Playback time: {value}")
            self.gui_manager.hide_loading()
            self.gui_manager.show_channel_info(self.current_channel_index, self.channels[self.current_channel_index]['name'])
            self.playback_time_printed = True

    def play_channel(self, index):
        url = self.channels[index]['url']
        if not url.strip():
            print(f"URL for {self.channels[index]['name']} is empty. Skipping.")
            return
        print(f"Playing {self.channels[index]['name']} - {url}")
        self.gui_manager.show_loading()
        self.playback_time_printed = False
        self.mpv.play(url)

    def reset_input_buffer(self):
        if self.input_buffer:
            try:
                index = int(self.input_buffer)
                if 0 <= index < len(self.channels):
                    print(f"Key {index} pressed")
                    self.gui_manager.update_number_window_label(self.input_buffer)
                    self.play_channel(index)
                    self.current_channel_index = index
            except ValueError:
                print("Invalid input buffer")
        self.input_buffer = ""
        if self.timer:
            self.timer.cancel()
            self.timer = None
        self.gui_manager.hide_number_window()

    def on_key_press(self, key):
        try:
            if key.char.isdigit():
                if len(self.input_buffer) < config.INPUT_BUFFER_MAX_LENGTH:
                    if self.timer:
                        self.timer.cancel()
                    self.input_buffer += key.char
                    self.gui_manager.update_number_window_label(self.input_buffer)
                    self.gui_manager.show_number_window()
                    self.timer = Timer(config.INPUT_RESET_TIMEOUT, self.reset_input_buffer)
                    self.timer.start()
        except AttributeError:
            pass
