# Quick Start Guide

Get the HTW Emerging Photo anonymization system up and running in minutes!

## 🚀 Fastest Way: Docker

**Prerequisites**: Docker and Docker Compose installed

```bash
# 1. Clone the repository
git clone <repository-url>
cd htw-emerging-photo

# 2. Start the application
docker-compose up --build

# 3. Access the application
# - Web UI: http://localhost:8501
# - API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

That's it! The system will:
- Download model weights automatically on first run
- Start the FastAPI backend on port 8000
- Start the Streamlit frontend on port 8501

## 🖥️ Local Development Setup

**Prerequisites**: Python 3.10+, pip

```bash
# 1. Clone and navigate
git clone <repository-url>
cd htw-emerging-photo

# 2. Run setup script
chmod +x scripts/setup.sh
./scripts/setup.sh

# 3. Activate virtual environment
source venv/bin/activate

# 4. Start backend (Terminal 1)
python main.py

# 5. Start frontend (Terminal 2 - new terminal)
source venv/bin/activate
streamlit run frontend/app.py
```

Access the application:
- Web UI: http://localhost:8501
- API: http://localhost:8000/docs

## 📸 Using the System

### Via Web Interface

1. Open http://localhost:8501 in your browser
2. Click "Browse files" or drag and drop an image
3. Click "🔒 Anonymize Image"
4. View the anonymized result with yellow-filled regions
5. Download the anonymized image if needed

### Via API

```bash
# Anonymize an image
curl -X POST "http://localhost:8000/api/v1/anonymize" \
  -F "file=@path/to/your/image.jpg" \
  -H "accept: application/json" \
  > result.json

# View API documentation
open http://localhost:8000/docs
```

### Via Python

```python
import requests

# Upload and anonymize
with open('image.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/v1/anonymize',
        files={'file': f}
    )

result = response.json()
print(f"Faces anonymized: {result['summary']['total_faces']}")
print(f"Plates anonymized: {result['summary']['total_plates']}")
```

## 🧪 Testing

```bash
# Run tests
make test

# Or manually
pytest tests/ -v
```

## 🛑 Stopping the Application

### Docker
```bash
# Stop containers
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Local
```bash
# Press Ctrl+C in each terminal running the backend/frontend
```

## 📊 What to Expect

- **Face Detection**: Yellow boxes over detected faces
- **License Plate Detection**: Yellow boxes over detected vehicles/plates
- **Processing Time**: 2-5 seconds per image (CPU)
- **Confidence Scores**: Displayed for each detection
- **Before/After**: Side-by-side comparison in the UI

## ⚙️ Configuration

Edit `.env` file to customize:

```bash
# Detection thresholds
FACE_CONFIDENCE_THRESHOLD=0.7    # 0.0 to 1.0
PLATE_CONFIDENCE_THRESHOLD=0.6   # 0.0 to 1.0

# Anonymization color
ANONYMIZATION_COLOR="#FFFF00"    # Hex color code

# File size limit
MAX_UPLOAD_SIZE=10485760         # Bytes (10MB)
```

## 🆘 Troubleshooting

### Models not downloading
```bash
# Manually trigger model download
python -c "from src.detection import FaceDetector, PlateDetector; FaceDetector(); PlateDetector()"
```

### Port already in use
```bash
# Change ports in .env
API_PORT=8001
STREAMLIT_SERVER_PORT=8502
```

### Out of memory
```bash
# Use smaller images or reduce batch size
# Images are automatically resized to max 4096x4096
```

### API not connecting
```bash
# Check if backend is running
curl http://localhost:8000/health

# Check logs
docker-compose logs backend
```

## 📚 Next Steps

- Read the [full README](README.md) for detailed information
- Explore [API documentation](http://localhost:8000/docs) when running
- Check [ARCHITECTURE.md](docs/ARCHITECTURE.md) for system design
- Review [REQUIREMENTS.md](docs/REQUIREMENTS.md) for specifications

## 💡 Tips

- Use JPG or PNG images (max 10MB)
- Better lighting = better detection
- Frontal faces work best
- Clear license plates are easier to detect
- Processing time increases with image size

Happy anonymizing! 🔒✨

