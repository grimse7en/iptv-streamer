import pyudev
import threading
import subprocess

class PowerManager:
    def __init__(self, player):
        self.context = pyudev.Context()
        self.monitor = pyudev.Monitor.from_netlink(self.context)
        self.monitor.filter_by(subsystem='drm')
        self.player = player

    def start_monitoring(self):
        observer = threading.Thread(target=self._monitor_events, daemon=True)
        observer.start()

    def _monitor_events(self):
        for device in iter(self.monitor.poll, None):
            if device.action == 'change' and 'card' in device.device_path:
                self.check_monitor_status()

    def check_monitor_status(self):
        try:
            result = subprocess.run(['xrandr'], capture_output=True, text=True)
            output = result.stdout
            if "DP-2 connected " in output:
                print("External monitor is turned on.")
            else:
                print("External monitor is turned off.")
                self.player.exit()
        except Exception as e:
            print(f"Error checking monitor status: {e}")
