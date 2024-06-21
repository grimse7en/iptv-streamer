import json
import time
import subprocess
from iptv_player import IPTVPlayer
from gui_manager import GUIManager
from input_manager import InputManager
from power_manager import PowerManager
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

def is_connected():
    try:
        result = subprocess.run(['nmcli', '-t', '-f', 'DEVICE,STATE', 'device'], stdout=subprocess.PIPE)
        output = result.stdout.decode()
        for line in output.splitlines():
            device, state = line.split(':')
            if state == 'connected':
                return True
    except Exception as e:
        print(f"An error occurred while checking the network connection: {e}")
    return False

def main():
    channels = load_channels('channels.json')
    if not channels:
        return

    gui_manager = GUIManager()
    player = IPTVPlayer(channels, gui_manager)
    input_manager = InputManager(player, gui_manager)

    power_manager = PowerManager(player)
    power_manager.start_monitoring()

    # Wait until internet connection is established
    print("Waiting for internet connection...")
    while not is_connected():
        time.sleep(1)
    print("Internet connection established.")

    print("Press keys 0-9 to switch channels. Press 'esc' to exit.")
    player.play_channel(config.DEFAULT_CHANNEL_INDEX)
    
    gui_manager.run()

if __name__ == "__main__":
    main()
