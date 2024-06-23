from pynput import keyboard
from threading import Timer
import config

class InputManager:
    def __init__(self, player, gui_manager):
        self.player = player
        self.gui_manager = gui_manager
        self.input_buffer = ""
        self.timer = None

        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()

        self.exit_listener = keyboard.Listener(on_press=self.on_exit_key_press)
        self.exit_listener.start()

    def reset_input_buffer(self):
        if self.input_buffer:
            try:
                index = int(self.input_buffer)
                if 0 <= index < len(self.player.channels):
                    print(f"Key {index} pressed")
                    self.gui_manager.update_number_window_label(self.input_buffer)
                    self.player.play_channel(index)
            except ValueError:
                print("Invalid input buffer")
        self.input_buffer = ""
        if self.timer:
            self.timer.cancel()
            self.timer = None
        self.gui_manager.hide_number_window()

    def on_key_press(self, key):
        try:
            if key.char.isdigit():
                if len(self.input_buffer) < config.INPUT_BUFFER_MAX_LENGTH:
                    if self.timer:
                        self.timer.cancel()
                    self.input_buffer += key.char
                    self.gui_manager.update_number_window_label(self.input_buffer)
                    self.gui_manager.show_number_window()
                    if self.input_buffer == "1":
                        self.timer = Timer(config.INPUT_RESET_TIMEOUT_FULL, self.reset_input_buffer)
                    else:
                        self.timer = Timer(config.INPUT_RESET_TIMEOUT_SHORT, self.reset_input_buffer)
                    self.timer.start()
        except AttributeError:
            pass

    def on_exit_key_press(self, key):
        if key == keyboard.Key.esc:
            self.player.exit()
            self.gui_manager.hide_channel_info()
