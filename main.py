import json
import subprocess
from iptv_player import IPTVPlayer
from gui_manager import GUIManager
from input_manager import InputManager

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

    gui_manager = GUIManager()
    player = IPTVPlayer(channels, gui_manager)
    input_manager = InputManager(player, gui_manager)

    gui_manager.setup_fullscreen_window(channels)
    gui_manager.show_fullscreen_window()
    gui_manager.run()

if __name__ == "__main__":
    main()
