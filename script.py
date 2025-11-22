import subprocess
import datetime

def screenshot():
    try:
        subprocess.run(["scrot", 'pic.jpg'])
        print(f"Saved screenshot as: pic.jpg")

    except Exception as e:
        print(f"Failed to capture screenshot with: {e}")

if __name__ == "__main__":
    screenshot()