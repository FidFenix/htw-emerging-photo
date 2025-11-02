# License Plate Detection Model

## Current Model

**morsetechlab/yolov11-license-plate-detection**

This is a specialized YOLOv11 model trained specifically for license plate detection.

### Features:
- Based on YOLOv11 (latest YOLO version)
- Trained on diverse license plate datasets
- Works with various plate types (US, European, Asian, etc.)
- High accuracy for clear, visible plates
- Optimized for real-world conditions

### Model Priority:

The system tries models in this order:

1. **morsetechlab/yolov11-license-plate-detection** ← Primary (NEW!)
2. keremberke/yolov8m-license-plate-detection
3. keremberke/yolov8s-license-plate-detection
4. keremberke/yolov8n-license-plate-detection

### Automatic Download:

The model will be automatically downloaded from Ultralytics Hub on first use.

### Configuration:

- **Confidence Threshold**: 0.4 (40%)
- **Device**: MPS (Apple Silicon) / CUDA (NVIDIA) / CPU
- **Fallback**: Two-stage detection (car → plate) if direct detection fails

### Performance:

- **Accuracy**: High (specialized model)
- **Speed**: Fast (YOLOv11 is optimized)
- **Size**: ~6-10MB (will be downloaded once)

### Usage:

The model is automatically used when you restart the backend with `ENABLE_PLATE_DETECTION=true`.

Check logs for:
```
Trying to download: morsetechlab/yolov11-license-plate-detection
✅ License plate model loaded successfully: morsetechlab/yolov11-license-plate-detection
```

### Expected Results:

- Detects license plates directly from images
- Works with European, US, and other plate types
- Minimal false positives
- High confidence scores for clear plates

### Troubleshooting:

If the model fails to download:
1. Check internet connection
2. Verify Ultralytics Hub access
3. System will automatically try fallback models
4. Two-stage detection (car → plate) will activate as last resort

