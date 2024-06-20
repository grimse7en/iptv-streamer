import json
from iptv_player import IPTVPlayer
from gui_manager import GUIManager
from input_manager import InputManager
import config

def load_channels(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data['channels']
    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")
    except json.JSONDecodeError:
        print("Error decoding the JSON file.")
    return []

def main():
    channels = load_channels('channels.json')
    if not channels:
        return
    
    # TODO check if internet connection established

    gui_manager = GUIManager()
    player = IPTVPlayer(channels, gui_manager)
    player.play_channel(config.DEFAULT_CHANNEL_INDEX)
    input_manager = InputManager(player, gui_manager)

    print("Press keys 0-9 to switch channels. Press 'esc' to exit.")
    gui_manager.run()

if __name__ == "__main__":
    main()
