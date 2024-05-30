import json
from pynput import keyboard
from iptv_player import IPTVPlayer
from gui_manager import GUIManager
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

def setup_listeners(player, gui_manager):
    listener = keyboard.Listener(on_press=player.on_key_press)
    listener.start()

    def on_exit_key_press(key):
        if key == keyboard.Key.esc:
            listener.stop()
            gui_manager.root.quit()
            return False

    exit_listener = keyboard.Listener(on_press=on_exit_key_press)
    exit_listener.start()

def main():
    channels = load_channels('channels.json')
    if not channels:
        return

    gui_manager = GUIManager()
    player = IPTVPlayer(channels, gui_manager)

    setup_listeners(player, gui_manager)

    print("Press keys 0-9 to switch channels. Press 'esc' to exit.")
    gui_manager.run()

if __name__ == "__main__":
    main()
