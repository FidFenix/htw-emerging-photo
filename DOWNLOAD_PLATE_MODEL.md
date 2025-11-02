# License Plate Detection Model

## Problem
The standard YOLOv8 model doesn't detect license plates accurately because it wasn't trained on license plate data.

## Solution
Download a pre-trained YOLOv8 license plate detection model.

## Option 1: Use Roboflow Model (Recommended)

1. Visit: https://universe.roboflow.com/roboflow-universe-projects/license-plate-recognition-rxg4e/model/4
2. Click "Download Dataset"
3. Select "YOLOv8" format
4. Download the model weights file (.pt)
5. Rename it to `license_plate_detector.pt`
6. Place it in: `data/models/license_plate_detector.pt`

## Option 2: Use Pre-trained Model from GitHub

```bash
cd data/models
wget https://github.com/computervisioneng/automatic-number-plate-recognition-python-yolov8/raw/main/license_plate_detector.pt
```

## Option 3: Train Your Own (Advanced)

```bash
# Install ultralytics
pip install ultralytics

# Train on license plate dataset
yolo task=detect mode=train model=yolov8n.pt data=license_plates.yaml epochs=100
```

## Quick Test Command

```bash
# After placing the model, restart the backend
# Check logs for: "Loading custom license plate model"
```

## For POC Without Custom Model

The application will work with fallback detection (less accurate) if no custom model is found.
To improve accuracy, please add a custom license plate model as described above.

