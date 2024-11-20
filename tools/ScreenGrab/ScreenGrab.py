"""
Simple tool to rapidly capture screenshots and save them in a local directory.
"""

import os, time, keyboard
from PIL import ImageGrab

KEY = '1'
SAVE_FOLDER = './tools/ScreenGrab/game_capture_images'

# Function to take a screenshot and save it in the corresponding folder
def take_screenshot(folder_name):
    # Create folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Take screenshot
    screenshot = ImageGrab.grab()

    # Create a unique filename based on the current timestamp
    # Use the timestamp so that no two images are ever capturied with the same name
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    file_path = os.path.join(folder_name, f"screenshot_{timestamp}.png")

    # Save the screenshot
    screenshot.save(file_path)
    print(f"Screenshot saved in folder '{folder_name}' as {file_path}")

# Main loop that listens for keypresses
def main():
    print(f"Press {KEY} to take a screenshot.")
    
    while True:
        try:
            if keyboard.is_pressed(KEY):
                take_screenshot(SAVE_FOLDER)
                time.sleep(1)

        except KeyboardInterrupt:
            print("Exiting program.")
            break

if __name__ == "__main__":
    main()