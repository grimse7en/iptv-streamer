import subprocess

def suspend_system(self):
    try:
        # Use systemctl to suspend the system
        subprocess.run(['systemctl', 'suspend'], check=True)
        print("System is going to suspend...")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while trying to suspend the system: {e}")