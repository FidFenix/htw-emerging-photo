# Alternative License Plate Detection Models

## Currently Configured Models (Auto-download)

The application will try these models in order:

1. **keremberke/yolov8m-license-plate-detection** (Medium - Best Accuracy)
   - Size: ~50MB
   - Accuracy: High
   - Speed: Medium
   - **Recommended for production**

2. **keremberke/yolov8s-license-plate-detection** (Small - Balanced)
   - Size: ~22MB
   - Accuracy: Good
   - Speed: Fast
   - **Good balance**

3. **keremberke/yolov8n-license-plate-detection** (Nano - Fastest)
   - Size: ~6MB
   - Accuracy: Moderate
   - Speed: Very Fast
   - **Good for POC**

## Other High-Quality Options

### Option 1: Roboflow Universe Models
Visit: https://universe.roboflow.com/

Popular models:
- `roboflow-universe-projects/license-plate-recognition-rxg4e`
- `augmented-startups/vehicle-registration-plates-trudk`

### Option 2: Train Your Own (Best Accuracy)

```bash
# Download a license plate dataset
# Example: CCPD (Chinese City Parking Dataset)
# Or ALPR datasets from Kaggle

# Train YOLOv8
yolo task=detect mode=train \
  model=yolov8m.pt \
  data=license_plates.yaml \
  epochs=100 \
  imgsz=640 \
  batch=16

# Save the trained model
# Place at: data/models/license_plate_detector.pt
```

### Option 3: Pre-trained from GitHub

```bash
# High-quality pre-trained models
cd data/models

# Option A: From Roboflow (if you have API key)
curl -L "YOUR_ROBOFLOW_MODEL_URL" -o license_plate_detector.pt

# Option B: From Kaggle (requires kaggle CLI)
kaggle datasets download -d andrewmvd/car-plate-detection
```

## Manual Download Instructions

If automatic download fails:

1. Go to: https://universe.roboflow.com/roboflow-universe-projects/license-plate-recognition-rxg4e/model/4
2. Click "Download Dataset"
3. Select "YOLOv8" format
4. Download the `.pt` file
5. Save as: `data/models/license_plate_detector.pt`
6. Restart backend

## Verify Model Quality

After loading, check logs for:
```
✅ License plate model loaded successfully: keremberke/yolov8m-license-plate-detection
YOLO model loaded successfully on MPS/CUDA/CPU
```

## Performance Comparison

| Model | Size | mAP@0.5 | Inference (CPU) | Inference (GPU) |
|-------|------|---------|-----------------|-----------------|
| YOLOv8n | 6MB | ~85% | 50ms | 10ms |
| YOLOv8s | 22MB | ~90% | 80ms | 15ms |
| YOLOv8m | 50MB | ~93% | 150ms | 25ms |
| YOLOv8l | 87MB | ~95% | 250ms | 40ms |

**Recommendation**: Use YOLOv8m for best balance of accuracy and speed.

