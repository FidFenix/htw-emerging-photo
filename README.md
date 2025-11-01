# HTW Emerging Photo - Face and License Plate Anonymization POC
### Group 4: 
### Project: Human-Face and License-Plate Anonymization

### Members:
- Fidel
- Deema
- Aiman
- Anup
- Sakshi
- Siddhant <br>

🔒 **AI-Powered Anonymization System** for automatically detecting and anonymizing faces and license plates in images using solid yellow color overlay.

## 🎯 Overview

This Proof of Concept (POC) demonstrates automated anonymization of sensitive information in surveillance imagery from public transport environments (bus stops, metro stations). The system uses state-of-the-art machine learning models to detect and completely obscure faces and license plates with yellow color fill (#FFFF00).

### Key Features

- 👤 **Face Detection & Anonymization**: RetinaFace model with ≥90% accuracy
- 🚗 **License Plate Detection & Anonymization**: YOLO model with ≥85% accuracy
- 🟨 **Complete Obscuration**: Solid yellow (#FFFF00) color fill for privacy protection
- 🌐 **REST API**: FastAPI backend for integration
- 🖥️ **Web Interface**: Streamlit UI with before/after visualization
- 🐳 **Docker Support**: Containerized deployment
- 📊 **Confidence Scores**: Per-detection confidence metrics

## 🏗️ Architecture

```
┌─────────────────┐
│  Streamlit UI   │  (Frontend - Port 8501)
└────────┬────────┘
         │
         │ HTTP
         ▼
┌─────────────────┐
│   FastAPI       │  (Backend - Port 8000)
│   /anonymize    │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌─────────┐ ┌──────────┐
│RetinaFace│ │   YOLO   │  (Detection Models)
└─────────┘ └──────────┘
         │
         ▼
    ┌──────────┐
    │Anonymizer│  (Yellow Fill #FFFF00)
    └──────────┘
```

## 📋 Requirements

- Python 3.10+
- Docker & Docker Compose (optional)
- 4GB+ RAM
- CPU (GPU optional but not required)

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd htw-emerging-photo

# Start with Docker Compose
docker-compose up --build

# Access the application
# - Frontend: http://localhost:8501
# - API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

### Option 2: Local Setup

```bash
# Run setup script
chmod +x scripts/setup.sh
./scripts/setup.sh

# Activate virtual environment
source venv/bin/activate

# Start backend (Terminal 1)
python main.py

# Start frontend (Terminal 2)
streamlit run frontend/app.py
```

## 📁 Project Structure

```
htw-emerging-photo/
├── src/
│   ├── api/                    # FastAPI application
│   │   ├── app.py             # App factory
│   │   └── routes/            # API endpoints
│   ├── detection/             # Detection models
│   │   ├── faces/             # Face detection (RetinaFace)
│   │   └── plates/            # Plate detection (YOLO)
│   ├── anonymization/         # Anonymization logic
│   ├── preprocessing/         # Image validation & preprocessing
│   ├── config/                # Configuration management
│   └── utils/                 # Utilities & exceptions
├── frontend/
│   └── app.py                 # Streamlit UI
├── tests/                     # Test suite
├── scripts/                   # Helper scripts
├── data/
│   ├── models/                # Model weights (auto-downloaded)
│   └── uploads/               # Temporary uploads
├── docs/                      # Documentation
├── Dockerfile                 # Backend container
├── Dockerfile.frontend        # Frontend container
├── docker-compose.yml         # Docker orchestration
├── requirements.txt           # Python dependencies
└── main.py                    # Entry point

```

## 🔧 Configuration

Configuration is managed via environment variables. Copy `.env.example` to `.env` and adjust as needed:

```bash
# Application
APP_NAME="HTW Emerging Photo"
DEBUG=false
LOG_LEVEL="INFO"

# API
API_HOST="0.0.0.0"
API_PORT=8000
MAX_UPLOAD_SIZE=10485760  # 10MB

# Detection
FACE_CONFIDENCE_THRESHOLD=0.7
PLATE_CONFIDENCE_THRESHOLD=0.6

# Anonymization
ANONYMIZATION_COLOR="#FFFF00"  # Yellow
```

## 📡 API Usage

### Anonymize Image

```bash
curl -X POST "http://localhost:8000/api/v1/anonymize" \
  -F "file=@image.jpg" \
  -H "accept: application/json"
```

### Response Format

```json
{
  "success": true,
  "processing_time": 1.23,
  "anonymized_image": "base64_encoded_image_data",
  "faces_anonymized": [
    {
      "id": 1,
      "bbox": {"x": 100, "y": 150, "width": 80, "height": 100},
      "confidence": 0.95,
      "anonymization_color": "#FFFF00"
    }
  ],
  "plates_anonymized": [
    {
      "id": 1,
      "bbox": {"x": 200, "y": 300, "width": 120, "height": 40},
      "confidence": 0.87,
      "anonymization_color": "#FFFF00"
    }
  ],
  "summary": {
    "total_faces": 1,
    "total_plates": 1,
    "total_anonymized": 2,
    "anonymization_color": "#FFFF00"
  }
}
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Or use the script
chmod +x scripts/run_tests.sh
./scripts/run_tests.sh
```

## 📊 Performance

- **Face Detection**: ≥90% precision (RetinaFace)
- **License Plate Detection**: ≥85% precision (YOLO)
- **Processing Time**: <5 seconds per image (CPU)
- **Anonymization Quality**: 100% obscuration with yellow fill
- **Supported Formats**: JPG, PNG
- **Max File Size**: 10MB

## 🔒 Privacy & Security

- **No Image Storage**: Images are not saved by default
- **No Content Logging**: Image content is never logged
- **Complete Obscuration**: Yellow fill completely hides sensitive regions
- **Confidence Filtering**: Only high-confidence detections are anonymized
- **Input Validation**: File type, size, and integrity checks

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:

- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - System architecture and design
- [REQUIREMENTS.md](docs/REQUIREMENTS.md) - Functional and non-functional requirements
- [PROCESSES.md](docs/PROCESSES.md) - Development processes and workflows
- [VALUE_PROPOSITION.md](docs/VALUE_PROPOSITION.md) - Project value and business case
- [PLANNING.md](docs/PLANNING.md) - Project planning and timeline

## 🛠️ Development

### Setup Development Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Run in development mode
DEBUG=true python main.py
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

## 🚧 Known Limitations (POC)

- Single image processing only (no batch upload)
- CPU-optimized inference (GPU support available but not required)
- Basic anonymization (solid color fill, not generative inpainting)
- Limited to JPG/PNG formats
- No real-time video processing
- Pre-trained models only (no custom training)

## 🔮 Future Enhancements (Phase 2)

- Advanced generative anonymization (Stable Diffusion inpainting)
- Realistic face/plate replacement instead of yellow fill
- Batch image processing
- Video stream support
- Real-time processing optimization
- Custom model training
- Multi-camera deployment

## 📄 License

This is a Proof of Concept project for educational purposes.

## 👥 Contributors

HTW Development Team

## 📞 Support

For issues or questions, please refer to the documentation in the `docs/` directory or contact the development team.

---

**Status**: 🔄 POC In Progress  
**Version**: 1.0.0  
**Last Updated**: November 1, 2025
