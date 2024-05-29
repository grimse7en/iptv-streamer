import json
from pynput import keyboard
from iptv_player import IPTVPlayer
from gui_manager import GUIManager

def main():
    try:
        with open('urls.json', 'r') as file:
            data = json.load(file)
            urls = data['urls']
    except FileNotFoundError:
        print("The file 'urls.json' was not found.")
        return
    except json.JSONDecodeError:
        print("Error decoding the JSON file.")
        return

    player = IPTVPlayer(urls)
    GUIManager.initialize(player)

    listener = keyboard.Listener(on_press=player.on_press)
    listener.start()

    print("Press keys 0-9 to switch channels. Press 'esc' to exit.")

    def on_press_exit(key):
        if key == keyboard.Key.esc:
            listener.stop()
            GUIManager.number_window.quit()
            return False

    with keyboard.Listener(on_press=on_press_exit) as exit_listener:
        GUIManager.number_window.mainloop()
        exit_listener

if __name__ == "__main__":
    main()
