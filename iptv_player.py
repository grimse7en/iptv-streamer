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
            print(f"Populating playlist")
            self.play_local_files(self.channels[self.current_channel_index].get('path', ''))

    def play_local_files(self, path):
        if path and os.path.isdir(path):
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            random.shuffle(files)  # Shuffle the list of files
            self.mpv.command('stop')  # Stop the current playback
            self.mpv.playlist_clear()  # Clear the playlist before adding new items
            for file in files:
                file_path = os.path.join(path, file)
                #print(f"Adding file to playlist: {file_path}")
                self.mpv.playlist_append(file_path)  # Add each file to the playlist
            self.mpv.playlist_pos = 0  # Set the playlist position to start playing from the first file
        else:
            print("Invalid path.")

    def play_channel(self, index):
        url = self.channels[index]['url']
        if not url.strip():
            print(f"URL for {self.channels[index]['name']} is empty. Skipping.")
            return

        self.current_channel_index = index

        # Print channel change information
        if self.previous_channel_index is not None:
            print(f"Changed from {self.previous_channel_index} to {self.current_channel_index}")
        
        if url == 'local': # If local channel
            self.play_local_files(self.channels[index].get('path', ''))
            self.gui_manager.show_channel_info(index, self.channels[index].get('name', ''))
            self.previous_channel_index = self.current_channel_index
            #print(f"Index: {self.current_channel_index}")
            return        

        #print(f"Playing {self.channels[index]['name']} - {url}")
        self.gui_manager.show_loading()
        self.playback_time_printed = False
        self.mpv.play(url)
        self.previous_channel_index = self.current_channel_index
        #print(f"Index: {self.current_channel_index}")
