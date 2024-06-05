import mpv
import config
import random
import os

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
        self.mpv.observe_property("playlist-pos", self.handle_playlist_pos)
        self.play_channel(self.current_channel_index)

    def handle_playback_time(self, name, value):
        if value is not None and value > 0.0 and not self.playback_time_printed:
            #print(f"Playback time: {value}")
            self.gui_manager.hide_loading()
            self.gui_manager.show_channel_info(self.current_channel_index, self.channels[self.current_channel_index]['name'])
            self.playback_time_printed = True

    def handle_playlist_pos(self, name, value):
        if value == -1 and self.current_channel_index == 0: # if finished playing local files on channel 0
            print(f"End of playlist")
            self.play_italian_music_videos(self.channels[0].get('path', ''))
        #print(f"Current position in playlist: {value}")
        #print(f"Current channel index {self.current_channel_index}")

    def play_italian_music_videos(self, path):
        # Special case for channel 0
        if path and os.path.isdir(path):
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            random.shuffle(files)  # Shuffle the list of files
            print("Files in channel 0 path (randomized order):", files)
            self.mpv.command('stop')  # Stop the current playback
            self.mpv.playlist_clear()  # Clear the playlist before adding new items
            for file in files:
                file_path = os.path.join(path, file)
                print(f"Adding file to playlist: {file_path}")
                self.mpv.playlist_append(file_path)  # Add each file to the playlist
            self.mpv.playlist_pos = 0  # Set the playlist position to start playing from the first file
        else:
            print("Invalid path for channel 0.")

    def play_channel(self, index):
        if index == 0:
            # Special case for channel 0
            self.play_italian_music_videos(self.channels[index].get('path', ''))
            self.gui_manager.show_channel_info(index, self.channels[index].get('name', ''))
            return

        url = self.channels[index]['url']
        if not url.strip():
            print(f"URL for {self.channels[index]['name']} is empty. Skipping.")
            return

        print(f"Playing {self.channels[index]['name']} - {url}")
        self.gui_manager.show_loading()
        self.playback_time_printed = False
        self.mpv.play(url)
