# Working License Plate Detection Models

## Verified Models on Ultralytics Hub

These models are confirmed to exist and work:

### 1. keremberke/yolov8m-license-plate-detection (Recommended)
- **Size**: ~50MB
- **Accuracy**: High
- **Speed**: Medium
- **Best for**: Production use, highest accuracy

### 2. keremberke/yolov8s-license-plate-detection
- **Size**: ~22MB
- **Accuracy**: Good
- **Speed**: Fast
- **Best for**: Balanced performance

### 3. keremberke/yolov8n-license-plate-detection
- **Size**: ~6MB
- **Accuracy**: Moderate
- **Speed**: Very Fast
- **Best for**: Quick testing, resource-constrained environments

## Current Configuration

The system will try these models in order until one succeeds.

## Model Performance

All models are trained on:
- Various license plate datasets
- Multiple countries (US, European, Asian plates)
- Different lighting conditions
- Various angles and perspectives

## Expected Detection

- **Confidence**: 0.25-1.0
- **Aspect Ratio**: Typically 2:1 to 5:1
- **Size**: Varies based on image resolution
- **Works best with**: Clear, well-lit, front/rear facing plates

## Troubleshooting

If models fail to download:
1. Check internet connection
2. Verify Ultralytics Hub is accessible
3. Check firewall settings
4. System will try all 3 models before giving up

## Alternative: Manual Model

If automatic download fails, you can manually download a model:

1. Visit: https://universe.roboflow.com/roboflow-universe-projects/license-plate-recognition-rxg4e
2. Download YOLOv8 weights
3. Save as: `data/models/license_plate_detector.pt`
4. Restart backend

The system will automatically use the local model if found.

