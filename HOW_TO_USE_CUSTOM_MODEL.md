# How to Use a Custom License Plate Detection Model

## Quick Start

1. **Get a YOLOv8 license plate detection model** (`.pt` file)
   
2. **Place it here:**
   ```
   data/models/license_plate_detector.pt
   ```

3. **Restart your backend**

4. **Done!** The application will automatically:
   - Detect the custom model
   - Use it for direct license plate detection
   - Anonymize detected plates with yellow color

## Where to Get a Model

### Option 1: Download from Roboflow
1. Visit: https://universe.roboflow.com/
2. Search for "license plate detection"
3. Download a YOLOv8 model
4. Rename to `license_plate_detector.pt`

### Option 2: Train Your Own
```bash
# Install ultralytics
pip install ultralytics

# Download a license plate dataset (e.g., from Roboflow)
# Train the model
yolo task=detect mode=train model=yolov8n.pt data=your_dataset.yaml epochs=50

# Copy the trained model
cp runs/detect/train/weights/best.pt data/models/license_plate_detector.pt
```

### Option 3: Use Pre-trained from Community
Search GitHub for:
- "yolov8 license plate detection"
- Look for `.pt` files in releases or repositories

## Verification

Check if your model is being used:

```bash
# Start your backend and look for this log message:
✅ Loading custom license plate model: data/models/license_plate_detector.pt
✅ Custom license plate model loaded - will detect plates directly
```

If you see this instead:
```
⚠️ No custom model found
Using standard YOLOv8n with two-stage detection
```

Then the model file is missing or too small (<1MB).

## Test Your Model

```python
from ultralytics import YOLO

# Load your model
model = YOLO('data/models/license_plate_detector.pt')

# Test on an image
results = model('path/to/car_image.jpg')

# Check detections
for r in results:
    print(f"Found {len(r.boxes)} license plates")
    for box in r.boxes:
        print(f"  Confidence: {box.conf[0]:.2f}")
        print(f"  Box: {box.xyxy[0]}")
```

## Current Behavior

### With Custom Model
- ✅ Direct license plate detection
- ✅ High accuracy (depends on model quality)
- ✅ Fast processing
- ✅ Automatic anonymization with yellow overlay

### Without Custom Model (Fallback)
- ⚙️ Two-stage detection (car → plate)
- ⚙️ Uses contour detection within vehicles
- ⚙️ May have false positives/negatives
- ⚙️ Still functional for POC

## File Requirements

- **Format**: PyTorch model file (`.pt`)
- **Size**: Must be > 1MB (to filter out HTML error pages)
- **Type**: YOLOv8 trained on license plate detection
- **Location**: Exactly at `data/models/license_plate_detector.pt`

## Troubleshooting

### Model not loading
```bash
# Check if file exists
ls -lh data/models/license_plate_detector.pt

# Should show size > 1MB
# If it shows HTML or is very small, re-download
```

### Model loads but no detections
- Model might be trained on different plate types
- Try lowering confidence threshold in settings
- Check model was trained on similar plates (US vs EU vs Asian)

### Want to switch back to two-stage detection
```bash
# Simply rename or remove the model
mv data/models/license_plate_detector.pt data/models/license_plate_detector.pt.backup

# Restart backend
```

## Summary

Just place your YOLOv8 license plate model at `data/models/license_plate_detector.pt` and restart. The application will automatically detect and use it for accurate license plate detection and anonymization!

