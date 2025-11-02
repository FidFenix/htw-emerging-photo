# Using YOLOv11 from Ultralytics Hub

## Overview

The system now uses Ultralytics Hub to load the YOLOv11 license plate detection model directly:

```python
from ultralytics import YOLO

model = YOLO("morsetechlab/yolov11-license-plate-detection")
```

## How It Works

1. **On first startup**, the backend will:
   - Check for a local custom model at `data/models/license_plate_detector.pt`
   - If not found, download YOLOv11 from Ultralytics Hub using the model ID
   - Cache the model automatically
   - Load the model for direct license plate detection

2. **On subsequent startups**:
   - Use the cached model (no re-download)
   - Fast startup time

3. **Fallback behavior**:
   - If Ultralytics Hub download fails, falls back to YOLOv8n with two-stage detection

## Expected Logs

### First Run (Downloading):
```
Loading YOLO model for license plate detection...
MPS (Apple Silicon GPU) detected
No custom model found. Trying to download from Ultralytics Hub...
Downloading YOLOv11 from morsetechlab/yolov11-license-plate-detection...
✅ YOLOv11 license plate model loaded from Ultralytics Hub
YOLO model loaded successfully on MPS
```

### Subsequent Runs (Using Cache):
```
Loading YOLO model for license plate detection...
MPS (Apple Silicon GPU) detected
No custom model found. Trying to download from Ultralytics Hub...
Downloading YOLOv11 from morsetechlab/yolov11-license-plate-detection...
✅ YOLOv11 license plate model loaded from Ultralytics Hub (cached)
YOLO model loaded successfully on MPS
```

### Fallback (If Download Fails):
```
Loading YOLO model for license plate detection...
MPS (Apple Silicon GPU) detected
No custom model found. Trying to download from Ultralytics Hub...
Downloading YOLOv11 from morsetechlab/yolov11-license-plate-detection...
⚠️ Failed to load from Ultralytics Hub: [error message]
Using YOLOv8n with two-stage detection (car → plate)
YOLO model loaded successfully on MPS
```

## Changes Made

### 1. Simplified Model Loading
- Removed `huggingface-hub` dependency
- Now uses Ultralytics' built-in Hub integration
- Simpler, more reliable code

### 2. Updated `src/detection/plates/detector.py`
```python
# Old approach (Hugging Face):
from huggingface_hub import hf_hub_download
model_path = hf_hub_download(repo_id="...", filename="best.pt")
self.model = YOLO(model_path)

# New approach (Ultralytics Hub):
self.model = YOLO("morsetechlab/yolov11-license-plate-detection")
```

### 3. Updated `requirements.txt`
- Removed `huggingface-hub==0.19.4`
- Kept `ultralytics==8.0.220` (already includes Hub support)

## Model Priority

The system checks models in this order:

1. **Local custom model**: `data/models/license_plate_detector.pt` (if exists)
2. **Ultralytics Hub**: `morsetechlab/yolov11-license-plate-detection` (auto-download)
3. **Fallback**: YOLOv8n with two-stage detection (car → plate)

## Override with Custom Model

To use your own model instead:

```bash
# Place your custom YOLOv8/v11 model here:
cp your_model.pt data/models/license_plate_detector.pt

# Restart backend
# Your custom model will be used instead
```

## Requirements

Just the standard Ultralytics package:

```bash
pip install ultralytics==8.0.220
```

Or install from requirements.txt:

```bash
pip install -r requirements.txt
```

## Benefits

✅ **Simpler code** - No extra dependencies  
✅ **Built-in caching** - Ultralytics handles caching automatically  
✅ **Better integration** - Uses Ultralytics' native Hub support  
✅ **Automatic updates** - Can pull model updates from Hub  
✅ **Fallback** - Gracefully falls back to YOLOv8n if download fails  

## Testing

To test the model:

```bash
# Start backend
python main.py

# Or with Docker
docker-compose up --build

# Check logs for successful model loading
# Upload a test image with a license plate
# Verify yellow anonymization overlay on the plate
```

## Troubleshooting

### Model fails to load from Ultralytics Hub
- Check internet connection
- Verify the model ID is correct: `morsetechlab/yolov11-license-plate-detection`
- System will automatically fall back to YOLOv8n

### Model loads but no detections
- Model might be trained on specific plate types (US, EU, Asian)
- Try lowering confidence threshold in settings
- Check that your test image has visible license plates

### Want to use a different Ultralytics Hub model
Update the model ID in `src/detection/plates/detector.py`:
```python
self.model = YOLO("your-username/your-model-name")
```

## Summary

The system now uses Ultralytics Hub's native integration to load the YOLOv11 license plate detection model, providing a simpler and more reliable solution! 🚀

