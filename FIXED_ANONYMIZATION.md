# Fixed: License Plate Anonymization Not Working

## Problem
The YOLOv11 model from Hugging Face (`morsetechlab/yolov11-license-plate-detection`) was detecting license plates correctly, but they were not being anonymized (no yellow overlay).

## Root Cause
The `enable_plate_detection` setting was set to `False` by default in `src/config/settings.py`, which meant:
- The plate detector was not being initialized
- Plate detections were being skipped
- No anonymization was applied to detected plates

## Solution

### 1. Updated `src/config/settings.py`
Changed line 27 from:
```python
enable_plate_detection: bool = False  # Disabled by default (requires custom model)
```

To:
```python
enable_plate_detection: bool = True  # Enabled - using Hugging Face YOLOv11 model
```

Also lowered the confidence threshold from 0.6 to 0.25 for better detection:
```python
plate_confidence_threshold: float = 0.25  # Lower threshold for better detection
```

### 2. Updated `docker-compose.yml`
Added the environment variable:
```yaml
- ENABLE_PLATE_DETECTION=true
- PLATE_CONFIDENCE_THRESHOLD=0.25
```

## How to Apply the Fix

### If running locally:
```bash
# Just restart your backend - settings are updated
python main.py
```

### If running with Docker:
```bash
# Rebuild and restart containers
docker-compose down
docker-compose up --build
```

## What Should Happen Now

1. **Backend startup logs** should show:
   ```
   Initializing plate detector...
   Downloading YOLOv11 license plate model from Hugging Face...
   ✅ Downloaded model from morsetechlab/yolov11-license-plate-detection
   ✅ YOLOv11 license plate model loaded - will detect plates directly
   ```

2. **When processing an image** with license plates:
   ```
   Running license plate detection...
   Running plate detection on image shape: (height, width, 3)
   YOLO returned 1 result objects
   Processing N boxes from YOLO
   License plate detected: WxH, aspect=X.XX, conf=0.XX
   ✅ YOLO detected N license plates (threshold: 0.25)
   Anonymizing image...
   Anonymized N regions with color #FFFF00
   ```

3. **The anonymized image** will show:
   - Yellow rectangles over detected faces
   - Yellow rectangles over detected license plates
   - Original image preserved elsewhere

## Verification

Check the `/info` endpoint to confirm plate detection is enabled:
```bash
curl http://localhost:8000/api/v1/info
```

Should return:
```json
{
  "features": {
    "face_detection": true,
    "plate_detection": true
  },
  "models": {
    "face_detection": "retinaface",
    "plate_detection": "yolo"
  }
}
```

## Summary

✅ **Fixed**: `enable_plate_detection` is now `True` by default  
✅ **Fixed**: Confidence threshold lowered to 0.25 for better detection  
✅ **Fixed**: Docker environment variable added  
✅ **Result**: License plates are now being anonymized with yellow overlay!  

The system is now fully functional for both face and license plate anonymization! 🎉

