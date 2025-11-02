# Manual License Plate Model Setup

## Problem
The model `morsetechlab/yolov11-license-plate-detection` doesn't exist on Ultralytics Hub or Hugging Face.

## Solution: Use Two-Stage Detection (Current Fallback)

The system is currently using **YOLOv8n with two-stage detection** as a fallback:
1. Detect vehicles (cars, trucks, buses)
2. Search for license plates within vehicle regions using contour detection

This should work for basic license plate anonymization.

## Option 1: Download a Pre-trained Model (Recommended)

### From Roboflow Universe (Best Option)

1. **Visit Roboflow Universe:**
   ```
   https://universe.roboflow.com/
   ```

2. **Search for "license plate detection"**

3. **Popular datasets with YOLOv8 models:**
   - Search: "license plate yolov8"
   - Look for models with:
     - Good accuracy (mAP > 80%)
     - Recent updates
     - Many downloads

4. **Download the model:**
   - Click on a dataset
   - Go to "Versions" → Select latest version
   - Click "Export" → Choose "YOLOv8" format
   - Download the weights file (usually `best.pt` or `weights/best.pt`)

5. **Save the model:**
   ```bash
   # Copy the downloaded model to:
   cp ~/Downloads/best.pt data/models/license_plate_detector.pt
   ```

6. **Restart backend:**
   ```bash
   python main.py
   ```

### Example Roboflow Datasets

Try searching for these on Roboflow:
- "Car License Plate Detection"
- "Vehicle Registration Plate"
- "ALPR Dataset"
- "License Plate Recognition"

## Option 2: Use Pre-trained from GitHub

### YOLOv8 License Plate Models on GitHub

Search GitHub for:
```
yolov8 license plate detection .pt
```

Look for repositories with:
- Pre-trained weights (`.pt` files)
- Recent commits
- Good documentation

### Example repositories to try:
1. Search: `yolov8 license plate detection`
2. Look for releases with `.pt` files
3. Download and save as `data/models/license_plate_detector.pt`

## Option 3: Train Your Own Model

If you have a dataset of license plate images:

```bash
# Install ultralytics
pip install ultralytics

# Prepare your dataset in YOLO format
# dataset/
#   ├── images/
#   │   ├── train/
#   │   └── val/
#   └── labels/
#       ├── train/
#       └── val/

# Create data.yaml
cat > data.yaml << EOF
train: dataset/images/train
val: dataset/images/val
nc: 1
names: ['license_plate']
EOF

# Train the model
yolo task=detect mode=train model=yolov8n.pt data=data.yaml epochs=100 imgsz=640

# Copy the trained model
cp runs/detect/train/weights/best.pt data/models/license_plate_detector.pt
```

## Option 4: Use Current Two-Stage Detection

The system is already working with the fallback method. To improve it:

### Lower the confidence threshold:

**In `src/config/settings.py`:**
```python
plate_confidence_threshold: float = 0.15  # Lower for more detections
```

**Or set environment variable:**
```bash
export PLATE_CONFIDENCE_THRESHOLD=0.15
```

### Test the current system:

```bash
# Start backend
python main.py

# Upload an image with a clear license plate
# The two-stage detection should find it
```

## Current System Status

✅ **Face detection**: Working with RetinaFace  
⚙️ **License plate detection**: Using YOLOv8n + two-stage detection (fallback)  
✅ **Anonymization**: Working with yellow overlay  

The system is functional, but accuracy may vary depending on:
- Image quality
- Plate visibility
- Plate type (US, EU, Asian formats differ)
- Lighting conditions

## Quick Test

To verify the current system works:

1. **Start backend:**
   ```bash
   python main.py
   ```

2. **Check logs for:**
   ```
   ⚠️ Failed to load from Ultralytics Hub
   Using YOLOv8n with two-stage detection (car → plate)
   YOLO model loaded successfully on MPS
   ```

3. **Upload a test image** with a visible license plate

4. **Check for detections:**
   ```
   Found N vehicles, searching for plates within them...
   Two-stage detection found N license plates
   ```

## Recommended Next Steps

1. **Try the current two-stage detection** - it may work well enough for your POC
2. **If accuracy is insufficient**, download a model from Roboflow Universe
3. **Save as** `data/models/license_plate_detector.pt`
4. **Restart** and the system will use your custom model

## Summary

Since no public pre-trained models are readily available via Ultralytics Hub or Hugging Face, you have three options:

1. ✅ **Use current fallback** (two-stage detection) - works now, moderate accuracy
2. 📥 **Download from Roboflow** - best accuracy, requires manual download
3. 🏋️ **Train your own** - best for specific use case, requires dataset

The system is currently functional with the two-stage fallback! 🚀

