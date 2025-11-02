# Setup License Plate Detection Model

## Quick Setup (Recommended)

Run this command in your terminal:

```bash
cd /Volumes/hack/projects/emerging/htw-emerging-photo

# Download from a working source
wget -O data/models/license_plate_detector.pt \
  "https://github.com/MuhammadMoinFaisal/Automatic_Number_Plate_Detection_Recognition_YOLOv8/raw/main/license_plate_detector.pt"
```

Or using curl:

```bash
cd /Volumes/hack/projects/emerging/htw-emerging-photo

curl -L -o data/models/license_plate_detector.pt \
  "https://github.com/MuhammadMoinFaisal/Automatic_Number_Plate_Detection_Recognition_YOLOv8/raw/main/license_plate_detector.pt"
```

## Alternative: Use Ultralytics Hub Model

If the above doesn't work, the application will automatically try to download from Ultralytics Hub on first use:
- Model: `keremberke/yolov8n-license-plate-detection`
- This happens automatically when you start the backend with `ENABLE_PLATE_DETECTION=true`

## Enable License Plate Detection

After downloading the model, set the environment variable:

```bash
# Add to your .env file or export:
export ENABLE_PLATE_DETECTION=true
```

## Verify Setup

```bash
# Check if model exists
ls -lh data/models/license_plate_detector.pt

# Should show a file around 6MB (not 287KB HTML file)
file data/models/license_plate_detector.pt
# Should say: "data" or "Zip archive data"
```

## Restart Backend

After setting up the model:

```bash
# If running locally:
python main.py

# If running in Docker:
docker-compose restart backend
```

Check the logs for:
```
Loading custom license plate model: data/models/license_plate_detector.pt
```

## Troubleshooting

If you see "HTML document" when checking the file:
```bash
rm data/models/license_plate_detector.pt
# Try the download again
```

If downloads fail, you can:
1. Visit: https://universe.roboflow.com/roboflow-universe-projects/license-plate-recognition-rxg4e
2. Download the model manually
3. Save as `data/models/license_plate_detector.pt`

