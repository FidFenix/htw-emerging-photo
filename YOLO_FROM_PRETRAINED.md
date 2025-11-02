# Using YOLO.from_pretrained() for Hugging Face Models

## Overview

The system now uses `YOLO.from_pretrained(repo_id)` to load license plate detection models directly from Hugging Face:

```python
from ultralytics import YOLO

model = YOLO.from_pretrained("morsetechlab/yolov11-license-plate-detection")
```

## How It Works

The system tries multiple Hugging Face repositories in order:

1. `morsetechlab/yolov11-license-plate-detection`
2. `keremberke/yolov8m-license-plate-detection`
3. `keremberke/yolov8n-license-plate-detection`
4. `nickmuchi/yolov5-license-plate-detection`

If all fail, it falls back to YOLOv8n with two-stage detection.

## Expected Logs

### Success Case:
```
Loading YOLO model for license plate detection...
MPS (Apple Silicon GPU) detected
No custom model found. Trying to download from Hugging Face...
Trying to download from Hugging Face: morsetechlab/yolov11-license-plate-detection...
✅ License plate model loaded from Hugging Face: morsetechlab/yolov11-license-plate-detection
YOLO model loaded successfully on MPS
```

### Fallback Case (if first model fails):
```
Loading YOLO model for license plate detection...
MPS (Apple Silicon GPU) detected
No custom model found. Trying to download from Hugging Face...
Trying to download from Hugging Face: morsetechlab/yolov11-license-plate-detection...
⚠️ Failed to load from morsetechlab/yolov11-license-plate-detection: [error]
Trying to download from Hugging Face: keremberke/yolov8m-license-plate-detection...
✅ License plate model loaded from Hugging Face: keremberke/yolov8m-license-plate-detection
YOLO model loaded successfully on MPS
```

### Complete Fallback (if all models fail):
```
Loading YOLO model for license plate detection...
MPS (Apple Silicon GPU) detected
No custom model found. Trying to download from Hugging Face...
Trying to download from Hugging Face: morsetechlab/yolov11-license-plate-detection...
⚠️ Failed to load from morsetechlab/yolov11-license-plate-detection: [error]
Trying to download from Hugging Face: keremberke/yolov8m-license-plate-detection...
⚠️ Failed to load from keremberke/yolov8m-license-plate-detection: [error]
...
⚠️ All Hugging Face models failed to load
================================================================================
Using YOLOv8n with two-stage detection (car → plate)
This fallback method works but may have lower accuracy.
================================================================================
YOLO model loaded successfully on MPS
```

## Model Priority

1. **Local custom model**: `data/models/license_plate_detector.pt` (highest priority)
2. **Hugging Face models** (tries in order):
   - `morsetechlab/yolov11-license-plate-detection`
   - `keremberke/yolov8m-license-plate-detection`
   - `keremberke/yolov8n-license-plate-detection`
   - `nickmuchi/yolov5-license-plate-detection`
3. **Fallback**: YOLOv8n with two-stage detection (lowest priority)

## Benefits of YOLO.from_pretrained()

✅ **Direct Hugging Face integration** - No manual downloads  
✅ **Automatic caching** - Models cached after first download  
✅ **Multiple fallbacks** - Tries several models automatically  
✅ **Simple API** - One-line model loading  
✅ **Robust** - Graceful fallback if all downloads fail  

## Testing

```bash
# Restart backend to try the new approach
python main.py

# Watch logs to see which model loads successfully
# Upload a test image with a license plate
# Verify yellow anonymization on the plate
```

## Adding More Models

To add more Hugging Face repositories to try, update the list in `src/detection/plates/detector.py`:

```python
hf_repo_ids = [
    "morsetechlab/yolov11-license-plate-detection",
    "keremberke/yolov8m-license-plate-detection",
    "keremberke/yolov8n-license-plate-detection",
    "nickmuchi/yolov5-license-plate-detection",
    "your-username/your-model-name",  # Add your own
]
```

## Manual Override

To use your own model instead of auto-downloading:

```bash
# Place your custom model here:
cp your_model.pt data/models/license_plate_detector.pt

# Restart backend
python main.py

# Your model will be used (highest priority)
```

## Troubleshooting

### All models fail to load
- Check internet connection
- Verify Hugging Face is accessible
- System will use two-stage fallback automatically

### Model loads but no detections
- Model might be trained on specific plate types
- Try lowering confidence threshold in settings
- Check image has visible license plates

### Want to use a specific model
Place it at `data/models/license_plate_detector.pt` to skip auto-download

## Summary

The system now uses `YOLO.from_pretrained()` to automatically try multiple Hugging Face models, providing a robust solution with automatic fallback! 🚀

