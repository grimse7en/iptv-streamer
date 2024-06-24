from m3u8_handler import create_m3u8, trim_m3u8
import os
import mpv
import config

class IPTVPlayer:
    def __init__(self, channels, gui_manager):
        self.channels = channels
        self.gui_manager = gui_manager
        self.current_channel_index = None
        self.current_filepath = ""
        self.is_loading = False
        self.is_exited = False

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
        if value is not None and value > 0.0 and self.is_loading:
            #print(f"Playback time: {value}")
            self.gui_manager.hide_loading()
            self.gui_manager.show_channel_info(self.current_channel_index, self.channels[self.current_channel_index]['name'])
            self.is_loading = False

            # seek to timestamp if local channel
            channel_directory = config.LOCAL_CHANNEL_DIRECTORIES.get(self.current_channel_index)
            if channel_directory is not None:
                timestamp_filepath = os.path.join(channel_directory, config.MPV_TIMESTAMP_FILENAME)
                if os.path.exists(timestamp_filepath):
                    with open(timestamp_filepath, 'r') as f:
                        saved_timestamp = int(f.read().strip())
                    if(saved_timestamp != 0):
                        self.mpv.seek(saved_timestamp, 'absolute')
                        print(f"Seeked to saved timestamp: {saved_timestamp} seconds")
                        os.remove(timestamp_filepath)

    def eof_replay(self, name, value):
        if self.current_channel_index is None or self.is_exited:
            return

        playlist_pos = value
        if playlist_pos == -1 and self.channels[self.current_channel_index]['url'].startswith('file'): # if local channel playlist is empty
            m3u8_path = create_m3u8(config.LOCAL_CHANNEL_DIRECTORIES.get(self.current_channel_index))
            self.current_filepath = m3u8_path
            self.play_channel(self.current_channel_index)

    def on_path_change(self, name, value):
        if name == 'path' and value is not None:
            self.current_filepath = value

    def play_channel(self, channel_index):
        url = self.channels[channel_index]['url']
        if not url.strip():
            print(f"URL for {self.channels[channel_index]['name']} is empty. Skipping.")
            return
        
        # Save local channel place in playlist
        if self.current_channel_index is not None:
            if self.channels[self.current_channel_index]['url'].startswith('file'): # if currently playing channel is local
                print("SAVE LOCAL CHANNEL STATE")
                self.save_local_channel_state()

        self.gui_manager.show_loading()
        self.is_loading = True
        self.is_exited = False
        print(f"Changed from {self.current_channel_index} to {channel_index}")
        self.current_channel_index = channel_index
        self.mpv.play(url)
        
    def save_local_channel_state(self):
        channel_directory = config.LOCAL_CHANNEL_DIRECTORIES.get(self.current_channel_index)
        m3u8_path = f"{channel_directory}/playlist.m3u8"
        if os.path.exists(m3u8_path) and m3u8_path != self.current_filepath:
            trim_m3u8(m3u8_path, self.current_filepath)

            if(self.mpv.time_pos is not None):
                # Get the current timestamp from mpv
                current_timestamp = int(self.mpv.time_pos)
                timestamp_filename = config.MPV_TIMESTAMP_FILENAME
                timestamp_filepath = os.path.join(channel_directory, timestamp_filename)

                # Save the timestamp to file
                with open(timestamp_filepath, 'w') as f:
                    f.write(str(current_timestamp))
                print(f"Timestamp saved to {timestamp_filepath}")

    def exit(self):
        if self.current_channel_index is not None:
            if self.channels[self.current_channel_index]['url'].startswith('file'): # if currently playing channel is local
                self.save_local_channel_state()
        try:
            self.mpv.stop(False)
            self.current_channel_index = None
            self.current_filepath = ""
            self.is_loading = False
            self.is_exited = True
            self.gui_manager.hide_loading()
            print("Exited")
        except Exception as e:
            print(f"Error while quitting MPV: {e}")
