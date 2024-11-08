"""
A simple tool to run some sample screenshots to test if the model is functional.
This isn't used now that the main application has reached a baseline functionality.
"""

import cv2
import numpy as np
from ultralytics import YOLO
import time
import winsound
import easyocr
import pyttsx3
import os
import keyboard

'''FILES = [
    './tools/ModelTest/test_img/2.png',
    './tools/ModelTest/test_img/3.png',
    './tools/ModelTest/test_img/4.png',
    './tools/ModelTest/test_img/1.png',
    './tools/ModelTest/test_img/5.png'
]'''

FILES = ['./tools/ModelTest/test_img/6.png']

SPEECHRATE = 250
engine = pyttsx3.init()
engine.setProperty('rate', SPEECHRATE)
reader = easyocr.Reader(['en'], gpu=True)

model = YOLO('./NoMansModel.pt')

def save_vis_image(image_path, x1, y1, x2, y2):
    image = cv2.imread(image_path)
    output_directory = './tools/ModelTest/result_images'

    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # (0, 255, 0) is the color (green), 2 is the thickness

    filename = os.path.basename(image_path)
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    output_path = os.path.join(output_directory, filename)
    
    cv2.imwrite(output_path, image)
    print(f"Image saved with bounding boxes at {output_path}")

def process_image(image_path):
    frame = cv2.imread(image_path)
    
    if frame is None:
        print(f"Error: Unable to load image from {image_path}")
        return

    results = model(frame)
    detected = False
    for result in results:
        for box in result.boxes:
            detected = True
            winsound.Beep(1000, 300)  # High-pitched beep (positive)

            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            save_vis_image(image_path, x1, y1, x2, y2)

            cropped_frame = frame[y1:y2, x1:x2]

            img_to_read = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2RGB)
            
            read_text = reader.readtext(img_to_read, detail=0)
            text = " ".join(read_text)
            print(text)
        
            engine.say(text)
            engine.runAndWait()
        
    if not detected:
        winsound.Beep(400, 300)   # Low-pitched beep (negative)

def main():
    while True:
        if keyboard.is_pressed('1'):
            for file in FILES:
                process_image(file)

        if keyboard.is_pressed('q'):
            print("Exiting...")
            break
    
if __name__ == "__main__":
    main()
