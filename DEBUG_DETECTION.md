# Debug License Plate Detection

## If license plates are not being detected:

### 1. Check Backend Logs

Look for these key messages:

```bash
# Model loading
Loading YOLO model for license plate detection...
Trying to download: morsetechlab/yolov11-license-plate-detection
✅ License plate model loaded successfully: morsetechlab/yolov11-license-plate-detection
YOLO model loaded successfully on MPS/CUDA/CPU
```

### 2. Check Detection Logs

When you upload an image, look for:

```bash
Running plate detection on image shape: (height, width, 3)
YOLO returned X result objects
Processing Y boxes from YOLO
```

**If you see "Processing 0 boxes"** → The model didn't detect anything

### 3. Common Issues

#### Issue: Model not loading
**Symptoms**: Error messages about model loading
**Solution**: 
- Check internet connection
- Model will try fallbacks automatically
- Check if `_is_custom_model` is True in logs

#### Issue: Model detects but filters out
**Symptoms**: "Processing X boxes" but "YOLO detected 0 plates"
**Solution**:
- Check confidence threshold (currently 0.25)
- Check aspect ratio logs
- Detections might be filtered as too small/wrong aspect

#### Issue: No detections at all
**Symptoms**: "Processing 0 boxes from YOLO"
**Solution**:
- Model might not be trained on your image type
- Try different image (clear, well-lit, front-facing)
- Enable two-stage detection

### 4. Test with Known Good Image

Try with an image that has:
- Clear, visible license plate
- Good lighting
- Front or rear view of vehicle
- Plate is at least 50x20 pixels
- Aspect ratio 2:1 to 5:1

### 5. Manual Testing

```python
# In Python console
from ultralytics import YOLO
model = YOLO('morsetechlab/yolov11-license-plate-detection')
results = model('your_image.jpg')
print(f"Detections: {len(results[0].boxes)}")
for box in results[0].boxes:
    print(f"Confidence: {box.conf[0]:.2f}, Box: {box.xyxy[0]}")
```

### 6. Current Settings

- **Confidence Threshold**: 0.25 (25%)
- **Minimum Size**: 10x5 pixels
- **Aspect Ratio**: 1.0 to 10.0 (very lenient)
- **Two-Stage Detection**: Disabled (trusting model)

### 7. Enable Debug Logging

Set `LOG_LEVEL=DEBUG` in `.env` to see all filtering decisions.

### 8. Fallback Options

If the model consistently fails:

1. **Lower confidence threshold** to 0.1
2. **Enable two-stage detection** (car → plate)
3. **Try different model** from the fallback list
4. **Use manual detection** (disable plate detection, annotate manually)

### 9. Check Model Output

The model should output:
- Class: 0 (license plate)
- Confidence: 0.25-1.0
- Bounding box: [x1, y1, x2, y2]

If the model outputs different classes, it might not be the right model.

### 10. Last Resort

If nothing works, you can:
- Disable license plate detection: `ENABLE_PLATE_DETECTION=false`
- Focus on face detection only
- Document as a known limitation for the POC

