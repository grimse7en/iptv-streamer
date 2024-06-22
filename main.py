import json
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

def is_connected_to_internet():
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

def check_internet_and_start_player(gui_manager, player):
    if is_connected_to_internet():
        print("Internet connection established.")
        print("Ready for input.")
        gui_manager.hide_loading()
        gui_manager.hide_message_window()
        #player.play_channel(config.DEFAULT_CHANNEL_INDEX)
    else:
        print("Waiting for internet connection...")
        gui_manager.show_loading()
        gui_manager.show_message_window("Please wait")
        gui_manager.root.after(1000, check_internet_and_start_player, gui_manager, player)

def main():
    channels = load_channels('channels.json')
    if not channels:
        return

    gui_manager = GUIManager()
    player = IPTVPlayer(channels, gui_manager)
    input_manager = InputManager(player, gui_manager)

    #power_manager = PowerManager(player)
    #power_manager.start_monitoring()

    gui_manager.setup_fullscreen_window(channels)
    gui_manager.show_fullscreen_window()
    gui_manager.root.after(1000, check_internet_and_start_player, gui_manager, player)
    gui_manager.run()

if __name__ == "__main__":
    main()
