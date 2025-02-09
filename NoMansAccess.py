# Standard library imports
import os
import time

# Third-party imports
import cv2
import keyboard
import easyocr
import pyttsx3
import numpy as np
from PIL import ImageGrab
from ultralytics import YOLO

# Local imports
# This settings file is intended for the end user to edit.
import settings

engine = pyttsx3.init()
engine.setProperty('rate', settings.SPEECHRATE)
engine.setProperty('volume', settings.VOICEVOLUME)
reader = easyocr.Reader(['en'], gpu=True)

# Load YOLOv8 model
model = YOLO('NoMansModel.pt')

def take_screenshot():
    # Take screenshot directly into memory
    screenshot = ImageGrab.grab()

    # Convert the screenshot to a format that OpenCV can use (from PIL to NumPy array)
    frame = np.array(screenshot)

    # Convert RGB to BGR (OpenCV uses BGR by default)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    return frame

def save_screenshot(frame):
    # Create a unique filename based on the current timestamp
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    file_path = os.path.join('./img/failed_detects/', f"screenshot_{timestamp}.png")

    # Save the screenshot
    cv2.imwrite(file_path, frame)
    print("Screenshot saved for failed detects.")

def read_aloud(img_to_read):
    text = ''
    read_text = reader.readtext(img_to_read, detail=0)
    text = " ".join(read_text)
    print(text)
    engine.say(text)
    engine.runAndWait()

def process_image(options):
    frame = take_screenshot()
    
    results = model(frame)

    detected = False
    for option in options:
        for result in results:
            for box in result.boxes:
                label = box.cls
                label_name = model.names[int(label)]

                if label_name == option:
                    #engine.say(detect_type)
                    #engine.runAndWait()
                    detected = True
                    # Strip the x y coordinates out of the found boxes in order to draw them in the image
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                    
                    # Crop the detected object from the frame using the bounding box coordinates
                    cropped_frame = frame[y1:y2, x1:x2]
                    img_to_read = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2RGB)
                    
                    # Read the text from the image
                    read_aloud(img_to_read)
                    return
            
    if not detected:
        save_screenshot(frame)

def main():
    # Main loop that listens for key press events
    while True:
        # Check for control key press
        if keyboard.is_pressed(settings.KEY1):
            process_image(settings.PRIORITY_QUEUE1)
    
        if keyboard.is_pressed(settings.KEY2):
            process_image(settings.PRIORITY_QUEUE2)
        
        if keyboard.is_pressed(settings.KEY3):
            save_screenshot(take_screenshot())

        # Exit if exit key is pressed
        if keyboard.is_pressed(settings.KEYQUIT):
            print("Exiting...")
            break
        time.sleep(0.01)

if __name__ == "__main__":
    main()
