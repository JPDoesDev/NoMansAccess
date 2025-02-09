"""
This tool queues up the prepared dataset, trains the model, and outputs the .pt model file.
"""

from ultralytics import YOLO

model = YOLO('yolov8n.pt')  # Or use 'yolov8s.pt', 'yolov8m.pt', etc.

results = model.train(
    data='datasets/model_data/data.yaml',     # Dataset YAML file path
    epochs=100,                               # Number of training epochs
    patience=100,                             # How many cycles to wait for no improvement until quitting
    workers=0,                                # Workers
    imgsz=1440,                               # Image size for training
    batch=0.70,                               # Batch size, utilize 70% of GPU
    name='NoMansModel',                       # Name of the project/model
    device='cuda'                             # Set device to GPU 
)

metrics = model.val()

model.save('./tools/ModelGen/NoMansModel.pt')  # Saves the model file for use in the main program
