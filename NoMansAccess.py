# Standard library imports
import os
import time

# Optional import for the optional debuging timing chirps
#import winsound

# Third-party imports
import cv2
import numpy as np
from PIL import ImageGrab
from ultralytics import YOLO
import keyboard
import easyocr
import pyttsx3

# Local imports
# This setting files is inteded for the end user to edit.
import settings

engine = pyttsx3.init()
engine.setProperty('rate', settings.SPEACHRATE)
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
    print("No menus detected, screenshot saved for failed detects.")

def read_aloud(img_to_read):
    text = ''
    read_text = reader.readtext(img_to_read, detail=0)
    text = " ".join(read_text)
    print(text)
    engine.say(text)
    engine.runAndWait()

'''
 This function was put in place to watch the menu tabes.
 I found this wasn't really necicary and just added overhead 
 but this could be re visited if needed.

def menu_watcher():
    global last_tab
    frame = take_screenshot()
    # Screen Capture Code Here
    results = model(frame)
    for result in results:
        for box in result.boxes:
            label = box.cls
            label_name = model.names[int(label)]

            if label_name == 'menu_labeld':
                #engine.say(detect_type)
                #engine.runAndWait()
                # Strip the x y cordinates out of the found boxes in order to draw them in the image
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                
                # Crop the detected object from the frame using the bounding box coordinates
                cropped_frame = frame[y1:y2, x1:x2]
                img_to_read = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2RGB)
                text = ''
                read_text = reader.readtext(img_to_read, detail=0)
                text = " ".join(read_text)
                print(f"Last found tab = {last_tab}")
                print(f"Current found tab = {text}")
                if text != last_tab and (text != None or text != ''):
                    print("Passed check, reading new tab.")
                    last_tab = text
                    # Read the text from the image
                    read_aloud(img_to_read)
                    return last_tab
'''

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
                    # Strip the x y cordinates out of the found boxes in order to draw them in the image
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
    #Print header

    #counter = 0
    #last_tab = ''

    # Main loop that listens for key press events
    while True:
        '''counter += 1
        if counter > 30:
            counter = 0        
            #Check if you can find a menu tab and if so, has it changed.
            menu_watcher()'''

        # Check if the '1' key is pressed
        if keyboard.is_pressed(settings.KEY1):
            process_image(settings.PRIORITY_QUEUE1)
    
        if keyboard.is_pressed(settings.KEY2):
            process_image(settings.PRIORITY_QUEUE2)
        
        if keyboard.is_pressed(settings.KEY3):
            save_screenshot(take_screenshot())

        # Exit if key is pressed
        if keyboard.is_pressed(settings.KEYQUIT):
            print("Exiting...")
            break
        time.sleep(0.01)

if __name__ == "__main__":
    main()