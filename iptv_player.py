from m3u8_handler import create_m3u8, trim_m3u8
import mpv
import config

class IPTVPlayer:
    def __init__(self, channels, gui_manager):
        self.channels = channels
        self.gui_manager = gui_manager
        self.current_channel_index = None
        self.current_filepath = ""
        self.playback_time_printed = False

        self.mpv = mpv.MPV(
            ytdl=True,
            fullscreen=True,
            input_default_bindings=False,
            user_agent="Mozilla/5.0"
        )
        
        self.mpv.observe_property("playback-time", self.handle_playback_time)
        self.mpv.observe_property("playlist-pos", self.eof_replay)
        self.mpv.observe_property('path', self.on_path_change)

    def handle_playback_time(self, name, value):
        if value is not None and value > 0.0 and not self.playback_time_printed:
            #print(f"Playback time: {value}")
            self.gui_manager.hide_loading()
            self.gui_manager.show_channel_info(self.current_channel_index, self.channels[self.current_channel_index]['name'])
            self.playback_time_printed = True

    def eof_replay(self, name, value):
        if self.current_channel_index is None:
            return

        playlist_pos = value
        if playlist_pos == -1 and self.channels[self.current_channel_index]['url'].startswith('file'): # if local channel playlist is empty
            # TODO re-create .m3u8
            create_m3u8(config.CHANNEL_DIRECTORIES.get(self.current_channel_index))
            self.play_channel(self.current_channel_index)

    def on_path_change(self, name, value):
        if name == 'path':
            self.current_filepath = value

    def play_channel(self, channel_index):
        url = self.channels[channel_index]['url']
        if not url.strip():
            print(f"URL for {self.channels[channel_index]['name']} is empty. Skipping.")
            return
        
        # Resume local channel position
        #if url.startswith('file'):
            # TODO resume from timestamp

        # Save local channel place in playlist
        if self.current_channel_index is not None:
            if self.channels[self.current_channel_index]['url'].startswith('file'): # if currently playing channel is local
                directory = config.CHANNEL_DIRECTORIES.get(self.current_channel_index)
                trim_m3u8(f"{directory}/playlist.m3u8", self.current_filepath)

        self.gui_manager.show_loading()
        self.playback_time_printed = False
        self.mpv.play(url)
        print(f"Changed from {self.current_channel_index} to {channel_index}")
        self.current_channel_index = channel_index
        