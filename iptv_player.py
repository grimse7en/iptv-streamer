import mpv
from threading import Timer
import config

class IPTVPlayer:
    def __init__(self, urls):
        self.urls = urls
        self.current_index = -1
        self.input_buffer = ""
        self.timer = None
        self.playback_time_printed = False

        self.player = mpv.MPV(
            ytdl=True,
            fullscreen=True,
            input_default_bindings=False,
            user_agent="Mozilla/5.0"
        )
        
        self.player.observe_property("playback-time", self.handle_playback_time)

    def set_gui_manager(self, gui_manager):
        self.gui_manager = gui_manager

    def handle_playback_time(self, name, value):
        if value is not None and value > 0.0 and not self.playback_time_printed:
            print(f"Playback time: {value}")
            self.gui_manager.hide_loading()
            self.gui_manager.show_channel_info(self.current_index, self.urls[self.current_index]['name'])
            self.playback_time_printed = True

    def play_url(self, index):
        url = self.urls[index]['url']
        if not url.strip():
            print(f"URL for {self.urls[index]['name']} is empty. Skipping.")
            return
        print(f"Playing {self.urls[index]['name']} - {url}")
        self.gui_manager.show_loading()
        self.playback_time_printed = False
        self.player.play(url)

    def reset_input_buffer(self):
        if self.input_buffer:
            try:
                index = int(self.input_buffer)
                if 0 <= index < len(self.urls):
                    print(f"Key {index} pressed")
                    self.gui_manager.update_number_window_label(self.input_buffer)
                    self.play_url(index)
                    self.current_index = index
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
