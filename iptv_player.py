import mpv
import config
import random
import os

class IPTVPlayer:
    def __init__(self, channels, gui_manager):
        self.channels = channels
        self.gui_manager = gui_manager
        self.current_channel_index = None
        self.previous_channel_index = None
        self.playback_time_printed = False

        self.mpv = mpv.MPV(
            ytdl=True,
            fullscreen=True,
            input_default_bindings=False,
            user_agent="Mozilla/5.0"
        )
        
        self.mpv.observe_property("playback-time", self.handle_playback_time)
        self.mpv.observe_property("playlist-pos", self.eof_replay)

    def handle_playback_time(self, name, value):
        if value is not None and value > 0.0 and not self.playback_time_printed:
            #print(f"Playback time: {value}")
            self.gui_manager.hide_loading()
            self.gui_manager.show_channel_info(self.current_channel_index, self.channels[self.current_channel_index]['name'])
            self.playback_time_printed = True

    def eof_replay(self, name, value):
        playlist_pos = value
        if playlist_pos == -1 and self.current_channel_index in (0, 1, 6): # if empty and on local channel
            print(f"EMPTY LOCAL")

    def play_channel(self, index):
        url = self.channels[index]['url']
        if not url.strip():
            print(f"URL for {self.channels[index]['name']} is empty. Skipping.")
            return

        self.current_channel_index = index


        # Resume local channel position
        #if url.startswith('file'):
            # TODO resume playlist position in .m3u8

        # Save local channel place in playlist
        #if self.previous_channel_index is not None:
            #print(f"Changed from {self.previous_channel_index} to {self.current_channel_index}")
            #if self.channels[self.previous_channel_index]['url'].startswith('file'): # if previous channel is local
                # TODO save position in .m3u8




        #print(f"Playing {self.channels[index]['name']} - {url}")
        self.gui_manager.show_loading()
        self.playback_time_printed = False
        self.mpv.play(url)
        self.previous_channel_index = self.current_channel_index
        #print(f"Index: {self.current_channel_index}")
