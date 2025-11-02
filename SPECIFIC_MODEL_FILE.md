# Using Specific Model File: license-plate-finetune-v1l.pt

## Updated Configuration

The system now specifically looks for `license-plate-finetune-v1l.pt` from the Hugging Face repository.

## How It Works

### Priority Order:
1. **First**: Look for `license-plate-finetune-v1l.pt` (specific file)
2. **Fallback**: Use first `.pt` file found if target not available

### Code Logic:
```python
# Try to find the specific model file first
target_filename = "license-plate-finetune-v1l.pt"

if target_filename in pt_files:
    filename = target_filename
    self.logger.info(f"Found target model: {filename}")
else:
    # Fall back to first .pt file found
    filename = pt_files[0]
    self.logger.info(f"Target model not found, using: {filename}")
```

## Expected Logs

### Success Case (Target Model Found):
```
Method 3: Trying hf_hub_download (list files + download)...
Listing available files in repository...
Found 2 .pt model file(s): ['best.pt', 'license-plate-finetune-v1l.pt']
Found target model: license-plate-finetune-v1l.pt
Downloading license-plate-finetune-v1l.pt from morsetechlab/yolov11-license-plate-detection...
Model downloaded to: /path/to/cache/license-plate-finetune-v1l.pt
Loading YOLO model from downloaded file...
✅ Model loaded successfully from license-plate-finetune-v1l.pt!
✅ License plate model loaded from Hugging Face: morsetechlab/yolov11-license-plate-detection
YOLO model loaded successfully on MPS
```

### Fallback Case (Target Not Found):
```
Method 3: Trying hf_hub_download (list files + download)...
Listing available files in repository...
Found 1 .pt model file(s): ['best.pt']
Target model not found, using: best.pt
Downloading best.pt from morsetechlab/yolov11-license-plate-detection...
Model downloaded to: /path/to/cache/best.pt
Loading YOLO model from downloaded file...
✅ Model loaded successfully from best.pt!
```

## Model Information

### File: `license-plate-finetune-v1l.pt`
- **Type**: YOLOv11 fine-tuned for license plate detection
- **Repository**: `morsetechlab/yolov11-license-plate-detection`
- **Expected Performance**: High accuracy on license plates
- **Size**: Varies (will be downloaded and cached)

## Testing

```bash
# Restart your backend
python main.py

# Watch logs for:
# "Found target model: license-plate-finetune-v1l.pt"
# "✅ Model loaded successfully from license-plate-finetune-v1l.pt!"

# Upload an image with a license plate
# Should see accurate detection and yellow anonymization
```

## Cache Location

After first download, the model is cached:
```
~/.cache/huggingface/hub/models--morsetechlab--yolov11-license-plate-detection/
```

Subsequent runs will use the cached version (no re-download).

## Manual Override

If you want to use a different model file, update the target filename in `src/detection/plates/detector.py`:

```python
target_filename = "your-model-name.pt"
```

## Troubleshooting

### Model file not found
- Check if `license-plate-finetune-v1l.pt` exists in the repository
- System will fall back to first `.pt` file found
- Check logs for "Target model not found, using: [filename]"

### Download fails
- Check internet connection
- Verify Hugging Face Hub is accessible
- System will fall back to YOLOv8n + two-stage detection

## Summary

✅ **Configured** to use `license-plate-finetune-v1l.pt` specifically  
✅ **Fallback** to first `.pt` file if target not found  
✅ **Cached** after first download for fast subsequent loads  
✅ **Ready** to provide accurate license plate detection!  

Restart your backend to load the specific model! 🚀

