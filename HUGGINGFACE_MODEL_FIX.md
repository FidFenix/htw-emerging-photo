# Fixed: Hugging Face Model 404 Error

## Problem
The model `morsetechlab/yolov11-license-plate-detection` doesn't exist on Hugging Face, causing a 404 error.

## Solution
Updated the code to try multiple Hugging Face repositories in order:

### Model Priority (in order):
1. **Local custom model**: `data/models/license_plate_detector.pt` (if exists)
2. **Hugging Face models** (tries in order):
   - `keremberke/yolov8m-license-plate-detection`
   - `keremberke/yolov8n-license-plate-detection`
   - `nickmuchi/yolov5-license-plate-detection`
3. **Fallback**: YOLOv8n with two-stage detection (car → plate)

## What Changed

### 1. Multiple Hugging Face Sources
The system now tries multiple repositories automatically:
```python
hf_repos = [
    ("keremberke/yolov8m-license-plate-detection", "best.pt"),
    ("keremberke/yolov8n-license-plate-detection", "best.pt"),
    ("nickmuchi/yolov5-license-plate-detection", "best.pt"),
]
```

### 2. Re-enabled Two-Stage Fallback
If all Hugging Face downloads fail, the system will:
- Use YOLOv8n to detect vehicles
- Search for license plates within vehicle regions using contour detection
- This provides basic functionality even without a specialized model

## Expected Behavior

### Success Case (Hugging Face model downloads):
```
No custom model found. Trying to download from available sources...
Trying to download from keremberke/yolov8m-license-plate-detection...
✅ Downloaded model from keremberke/yolov8m-license-plate-detection
✅ License plate model loaded - will detect plates directly
YOLO model loaded successfully on MPS
```

### Fallback Case (All downloads fail):
```
No custom model found. Trying to download from available sources...
Trying to download from keremberke/yolov8m-license-plate-detection...
⚠️ Failed to download from keremberke/yolov8m-license-plate-detection: 404
Trying to download from keremberke/yolov8n-license-plate-detection...
⚠️ Failed to download from keremberke/yolov8n-license-plate-detection: 404
⚠️ All Hugging Face models failed to download
Using YOLOv8n with two-stage detection (car → plate)
💡 For better accuracy, manually download a license plate model to: data/models/license_plate_detector.pt
YOLO model loaded successfully on MPS
```

## Manual Model Download (Best Option)

For the most reliable setup, manually download a model:

### Option 1: From Roboflow Universe
1. Visit: https://universe.roboflow.com/
2. Search for "license plate detection"
3. Find a YOLOv8 model with good reviews
4. Download the weights (`.pt` file)
5. Save as `data/models/license_plate_detector.pt`

### Option 2: From Ultralytics Hub
1. Visit: https://hub.ultralytics.com/
2. Search for license plate detection models
3. Download a pre-trained model
4. Save as `data/models/license_plate_detector.pt`

### Option 3: Train Your Own
```bash
# Install ultralytics
pip install ultralytics

# Download a license plate dataset from Roboflow
# Train the model
yolo task=detect mode=train model=yolov8n.pt data=your_dataset.yaml epochs=50

# Copy the trained model
cp runs/detect/train/weights/best.pt data/models/license_plate_detector.pt
```

## Restart After Fix

```bash
# If running locally:
python main.py

# If running with Docker:
docker-compose down
docker-compose up --build
```

## Summary

✅ **Fixed**: System now tries multiple Hugging Face repositories  
✅ **Fixed**: Two-stage fallback re-enabled for robustness  
✅ **Improved**: Better error messages and troubleshooting tips  
✅ **Fallback**: Works even without specialized model (using YOLOv8n + contours)  

The system is now more resilient and will work even if Hugging Face models are unavailable! 🚀

