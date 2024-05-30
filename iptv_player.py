import mpv
import config

class IPTVPlayer:
    def __init__(self, channels, gui_manager):
        self.channels = channels
        self.gui_manager = gui_manager
        self.current_channel_index = config.DEFAULT_CHANNEL_INDEX
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
