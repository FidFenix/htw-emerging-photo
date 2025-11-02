# ADR-001: License Plate Detection Model Selection

## Status
**Accepted** - November 2, 2025

## Context

The HTW Emerging Photo POC requires license plate detection and anonymization capabilities. License plates are small objects with specific characteristics (rectangular shape, text content, variable aspect ratios across regions) that require specialized detection models.

### Problem Statement

Standard object detection models like YOLOv8 and YOLOv11 (base versions) do not include license plate detection in their pre-trained classes. They are trained on COCO dataset which includes 80 common object categories (person, car, bicycle, etc.) but does not include license plates as a distinct class.

### Requirements

- Detect license plates in various orientations and lighting conditions
- Support multiple license plate formats (US, European, Asian)
- Maintain acceptable accuracy for POC demonstration
- Integrate seamlessly with existing YOLO-based detection pipeline
- Minimize model download size and inference time

### Options Considered

1. **YOLOv8 Base Model (yolov8n.pt)**
   - Pre-trained on COCO dataset (80 classes)
   - Does NOT include license plate detection
   - Would require two-stage detection (detect car → find plate within car region using heuristics)
   - Lower accuracy, more complex implementation

2. **YOLOv11 Base Model**
   - Latest YOLO architecture with improved performance
   - Pre-trained on COCO dataset (80 classes)
   - Does NOT include license plate detection
   - Same limitations as YOLOv8 base

3. **OpenALPR (Automatic License Plate Recognition)**
   - Specialized library for license plate detection and OCR
   - Requires separate installation and dependencies
   - Commercial licensing for production use
   - Overkill for anonymization (includes OCR which we don't need)
   - Complex integration

4. **Fine-tuned YOLOv11 Model: morsetechlab/yolov11-license-plate-detection**
   - YOLOv11 architecture fine-tuned specifically for license plate detection
   - Available on Hugging Face Hub
   - Direct license plate detection without two-stage approach
   - Compatible with Ultralytics YOLO API
   - Open source and free to use

## Decision

**We will use the fine-tuned YOLOv11 model: `morsetechlab/yolov11-license-plate-detection`**

This model is downloaded from Hugging Face Hub and provides specialized license plate detection capabilities.

### Implementation Details

```python
# Model loading in src/detection/plates/detector.py
from huggingface_hub import hf_hub_download, list_repo_files
from ultralytics import YOLO

repo_id = "morsetechlab/yolov11-license-plate-detection"

# Download model file from Hugging Face
files = list_repo_files(repo_id)
pt_files = [f for f in files if f.endswith('.pt')]
model_file = hf_hub_download(repo_id=repo_id, filename=pt_files[0])

# Load YOLO model
model = YOLO(model_file)
```

### Model Characteristics

- **Architecture**: YOLOv11 (latest YOLO version with C3k2 modules)
- **Training**: Fine-tuned on license plate dataset
- **Classes**: Specialized for license plate detection
- **Format**: PyTorch (.pt) format
- **Size**: Optimized for inference speed
- **Confidence Threshold**: 0.20 (configurable)

## Consequences

### Positive

1. **Direct Detection**: No need for two-stage detection (car → plate)
2. **Higher Accuracy**: Model trained specifically for license plates
3. **Simpler Code**: Single detection pass, cleaner implementation
4. **Better Coverage**: Detects plates across various formats and conditions
5. **Easy Integration**: Compatible with existing Ultralytics YOLO API
6. **Open Source**: No licensing costs or restrictions
7. **Automatic Download**: Model downloaded on first use via Hugging Face Hub
8. **GPU Support**: Works with MPS (Apple Silicon), CUDA (NVIDIA), and CPU

### Negative

1. **Model Download**: First-time use requires downloading model (~10-50MB)
2. **Internet Dependency**: Requires internet connection on first run
3. **Hugging Face Dependency**: Adds `huggingface-hub` as a dependency
4. **Third-party Model**: Relies on external model repository
5. **Partial Detection**: Model sometimes detects only text portion of plate, requiring expansion logic

### Mitigations

1. **Model Caching**: Downloaded model is cached locally in `data/models/` directory
2. **Fallback Strategy**: If download fails, system falls back to YOLOv8n with two-stage detection
3. **Offline Support**: Once downloaded, model works offline
4. **Expansion Logic**: Anonymizer applies 2.5x width expansion to compensate for partial detections
5. **Local Model Option**: Users can manually download and place model in `data/models/license_plate_detector.pt`

## Alternatives Considered

### Alternative 1: Two-Stage Detection with YOLOv8n
```python
# Detect vehicles first
vehicles = yolo.detect(image, classes=['car', 'truck', 'bus'])

# For each vehicle, search for plate-like regions using:
# - Contour detection
# - Aspect ratio filtering (2:1 to 6:1)
# - Edge density analysis
# - Text region detection
```

**Rejected because:**
- Lower accuracy (many false positives/negatives)
- Complex implementation with multiple heuristics
- Slower inference (two passes)
- Difficult to tune for different plate types

### Alternative 2: OpenALPR
```python
from openalpr import Alpr

alpr = Alpr("us", "/path/to/config", "/path/to/runtime_data")
results = alpr.recognize_ndarray(image)
```

**Rejected because:**
- Requires system-level installation (not pip-installable)
- Commercial licensing for production
- Includes OCR (not needed for anonymization)
- More complex setup and dependencies
- Overkill for our use case

### Alternative 3: Train Custom YOLOv8 Model
**Rejected because:**
- Requires labeled dataset (time-consuming)
- Requires training infrastructure (GPU, time)
- Outside scope of POC
- Fine-tuned models already available

## Technical Specifications

### Dependencies
```txt
ultralytics>=8.3.0  # Required for YOLOv11 support (C3k2 module)
huggingface-hub==0.19.4  # For model download
torch>=2.0.0  # PyTorch backend
```

### Configuration
```python
# src/config/settings.py
plate_detection_model: str = "morsetechlab/yolov11-license-plate-detection"
plate_confidence_threshold: float = 0.20
enable_plate_detection: bool = True
```

### Model Storage
```
data/
└── models/
    ├── license_plate_detector.pt  # Custom model (if provided)
    └── [cached HF models]          # Auto-downloaded models
```

## References

- **Hugging Face Model**: https://huggingface.co/morsetechlab/yolov11-license-plate-detection
- **YOLOv11 Documentation**: https://docs.ultralytics.com/models/yolo11/
- **Ultralytics GitHub**: https://github.com/ultralytics/ultralytics
- **COCO Dataset Classes**: https://cocodataset.org/#explore (no license plate class)

## Related Documents

- `ARCHITECTURE.md` - System architecture overview
- `REQUIREMENTS.md` - FR-2: License Plate Detection Requirements
- `HOW_TO_USE_CUSTOM_MODEL.md` - Instructions for using alternative models

## Revision History

| Date | Version | Author | Changes |
|------|---------|--------|---------|
| 2025-11-02 | 1.0 | HTW Team | Initial ADR for license plate model selection |

---

**Decision Maker**: HTW Development Team  
**Stakeholders**: Backend developers, ML engineers, End users  
**Review Date**: End of POC phase

