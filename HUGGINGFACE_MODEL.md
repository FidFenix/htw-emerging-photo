# Using Hugging Face YOLOv11 License Plate Detection Model

## Overview

The system is now configured to automatically download and use the **YOLOv11 license plate detection model** from Hugging Face:

- **Repository**: `morsetechlab/yolov11-license-plate-detection`
- **Model**: YOLOv11 trained specifically for license plate detection
- **Source**: Hugging Face Hub

## How It Works

1. **On first startup**, the backend will:
   - Check for a local custom model at `data/models/license_plate_detector.pt`
   - If not found, download YOLOv11 from Hugging Face
   - Cache the model in `data/models/huggingface_cache/`
   - Load the model for direct license plate detection

2. **On subsequent startups**:
   - Use the cached model (no re-download)
   - Fast startup time

3. **Fallback behavior**:
   - If Hugging Face download fails, falls back to YOLOv8n with two-stage detection

## Expected Logs

### First Run (Downloading):
```
Loading YOLO model for license plate detection...
MPS (Apple Silicon GPU) detected
Downloading YOLOv11 license plate model from Hugging Face...
✅ Downloaded model from morsetechlab/yolov11-license-plate-detection
Model path: data/models/huggingface_cache/.../best.pt
✅ YOLOv11 license plate model loaded - will detect plates directly
YOLO model loaded successfully on MPS
```

### Subsequent Runs (Using Cache):
```
Loading YOLO model for license plate detection...
MPS (Apple Silicon GPU) detected
Downloading YOLOv11 license plate model from Hugging Face...
✅ Downloaded model from morsetechlab/yolov11-license-plate-detection
Model path: data/models/huggingface_cache/.../best.pt (cached)
✅ YOLOv11 license plate model loaded - will detect plates directly
YOLO model loaded successfully on MPS
```

### Fallback (If Download Fails):
```
Loading YOLO model for license plate detection...
MPS (Apple Silicon GPU) detected
Downloading YOLOv11 license plate model from Hugging Face...
⚠️ Failed to download Hugging Face model: [error message]
Falling back to YOLOv8n with two-stage detection
YOLO model loaded successfully on MPS
```

## Requirements

Make sure `huggingface-hub` is installed:

```bash
pip install huggingface-hub==0.19.4
```

Or install from requirements.txt:

```bash
pip install -r requirements.txt
```

## Model Priority

The system checks models in this order:

1. **Local custom model**: `data/models/license_plate_detector.pt` (if exists)
2. **Hugging Face YOLOv11**: `morsetechlab/yolov11-license-plate-detection` (auto-download)
3. **Fallback**: YOLOv8n with two-stage detection (car → plate)

## Override with Custom Model

To use your own model instead of the Hugging Face one:

```bash
# Place your custom YOLOv8/v11 model here:
cp your_model.pt data/models/license_plate_detector.pt

# Restart backend
# Your custom model will be used instead of downloading from Hugging Face
```

## Benefits

✅ **Automatic setup** - No manual model download required  
✅ **Specialized model** - Trained specifically for license plates  
✅ **Better accuracy** - YOLOv11 architecture with plate-specific training  
✅ **Cached** - Only downloads once, then uses cached version  
✅ **Fallback** - Gracefully falls back to YOLOv8n if download fails  
✅ **GPU support** - Works with MPS (Apple Silicon) and CUDA (NVIDIA)  

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

### Download fails with network error
- Check internet connection
- Try again (Hugging Face Hub has retry logic)
- System will fall back to YOLOv8n automatically

### Model loads but no detections
- Model might be trained on specific plate types (US, EU, Asian)
- Try lowering confidence threshold in settings
- Check that your test image has visible license plates

### Want to disable Hugging Face download
```bash
# Create an empty placeholder file to skip download
touch data/models/license_plate_detector.pt

# System will try to load it, fail, and use YOLOv8n fallback
# Or place a real custom model there
```

## Summary

The system now automatically downloads and uses a specialized YOLOv11 license plate detection model from Hugging Face, providing better accuracy than the previous two-stage approach, with no manual setup required! 🚀

