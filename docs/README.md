# HTW Emerging Photo - Documentation

## Overview

This directory contains comprehensive documentation for the HTW Emerging Photo POC - a system for anonymizing faces and license plates in images.

## Documentation Structure

### Core Documents

1. **[REQUIREMENTS.md](REQUIREMENTS.md)**
   - Functional requirements (FR-1 to FR-4)
   - Non-functional requirements (NFR-1 to NFR-3)
   - Success criteria
   - Acceptance criteria

2. **[ARCHITECTURE.md](ARCHITECTURE.md)**
   - System architecture overview
   - Component architecture (Frontend, API, Processing, Detection layers)
   - Data flow diagrams
   - Technology stack
   - Design decisions (ADR-001 to ADR-010)
   - Security and performance considerations

3. **[PROCESSES.md](PROCESSES.md)**
   - Development workflow
   - Anonymization request flow (sequence diagrams)
   - Model selection criteria
   - Deployment processes
   - Security and privacy guidelines

4. **[PLANNING.md](PLANNING.md)**
   - Project timeline and milestones
   - Sprint planning (4 sessions)
   - User stories and epics
   - User journey map
   - Risk management
   - Success metrics

5. **[VALUE_PROPOSITION.md](VALUE_PROPOSITION.md)**
   - Project goals and objectives
   - Target users and use cases
   - Pain points addressed
   - Project scope and constraints
   - Expected outcomes

### Architecture Decision Records (ADRs)

6. **[ADR-001-LICENSE-PLATE-DETECTION-MODEL.md](ADR-001-LICENSE-PLATE-DETECTION-MODEL.md)** ⭐ **NEW**
   - **Decision**: Use YOLOv11 fine-tuned model (`morsetechlab/yolov11-license-plate-detection`)
   - **Rationale**: Standard YOLO models (YOLOv8, YOLOv11) do NOT include license plate detection
   - **Context**: COCO dataset (80 classes) does not include license plates
   - **Alternatives**: Two-stage detection, OpenALPR, custom training
   - **Implementation**: Auto-download from Hugging Face Hub
   - **Status**: Accepted (November 2, 2025)

### Additional ADRs (in ARCHITECTURE.md)

- **ADR-001**: Use Streamlit for Frontend
- **ADR-002**: Use FastAPI for Backend
- **ADR-003**: Use PyTorch for ML
- **ADR-004**: No Image Storage
- **ADR-005**: Use Pre-trained Models
- **ADR-006**: Synchronous Processing
- **ADR-007**: RetinaFace for Faces
- **ADR-008**: YOLOv11 Fine-tuned Model for License Plate Detection (Updated)
- **ADR-009**: Docker Deployment
- **ADR-010**: Yellow Color Anonymization

## Key Technical Decisions

### Models

| Component | Model | Source | Rationale |
|-----------|-------|--------|-----------|
| Face Detection | RetinaFace | `insightface` library | State-of-the-art accuracy (>90%), robust to various conditions |
| License Plate Detection | YOLOv11 (Fine-tuned) | `morsetechlab/yolov11-license-plate-detection` (Hugging Face) | Specialized for license plates, base YOLO models lack this capability |

### Technology Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Frontend | Streamlit | Latest | Simple Python-based UI |
| Backend API | FastAPI | Latest | Modern async REST API |
| ML Framework | PyTorch | ≥2.0.0 | Model inference |
| Object Detection | Ultralytics YOLO | ≥8.3.0 | YOLOv11 support (C3k2 modules) |
| Model Hub | Hugging Face Hub | 0.19.4 | Model download |
| Face Detection | insightface | Latest | RetinaFace implementation |
| Image Processing | Pillow, OpenCV | Latest | Image manipulation |
| Web Server | Uvicorn (WSGI: Gunicorn) | Latest | ASGI/WSGI server |
| Containerization | Docker | Latest | Consistent deployment |

## Why YOLOv11 Fine-tuned Model?

### Problem
- **YOLOv8** and **YOLOv11** base models are trained on COCO dataset (80 classes)
- COCO dataset includes: person, car, bicycle, truck, etc.
- **COCO does NOT include license plates as a class**

### Solution
- Use **fine-tuned YOLOv11** model specifically trained for license plate detection
- Model: `morsetechlab/yolov11-license-plate-detection`
- Source: Hugging Face Hub
- Auto-downloaded on first use

### Benefits
1. ✅ Direct license plate detection (no two-stage approach needed)
2. ✅ Higher accuracy than heuristic-based detection
3. ✅ Simpler implementation
4. ✅ Open source and free
5. ✅ Compatible with existing YOLO API

### Trade-offs
1. ⚠️ Requires internet connection on first run (for model download)
2. ⚠️ Model sometimes detects only text portion (requires expansion logic)
3. ⚠️ Depends on third-party model repository

See [ADR-001](ADR-001-LICENSE-PLATE-DETECTION-MODEL.md) for complete details.

## Quick Links

### For Developers
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design and components
- [PROCESSES.md](PROCESSES.md) - Development workflow
- [ADR-001](ADR-001-LICENSE-PLATE-DETECTION-MODEL.md) - License plate model selection

### For Project Managers
- [PLANNING.md](PLANNING.md) - Timeline and milestones
- [VALUE_PROPOSITION.md](VALUE_PROPOSITION.md) - Project goals and scope

### For Stakeholders
- [REQUIREMENTS.md](REQUIREMENTS.md) - What the system does
- [VALUE_PROPOSITION.md](VALUE_PROPOSITION.md) - Business value

## Documentation Updates

### November 2, 2025
- ✅ Created ADR-001 for license plate detection model selection
- ✅ Updated ARCHITECTURE.md to reference YOLOv11 fine-tuned model
- ✅ Updated PROCESSES.md to specify YOLOv11
- ✅ Updated ADR-008 in ARCHITECTURE.md with YOLOv11 details
- ✅ Updated architecture diagrams to show YOLOv11
- ✅ Updated model storage documentation
- ✅ Created this README.md

### October 20, 2025
- Initial documentation created
- Requirements, architecture, processes, planning, and value proposition defined
- Design decisions documented (ADR-001 to ADR-010)

## Document Maintenance

### Review Schedule
- **Weekly**: During POC development (Sessions 1-4)
- **Post-POC**: Final review and updates
- **As Needed**: When architectural decisions change

### Change Process
1. Identify need for documentation update
2. Update relevant document(s)
3. Create/update ADR if architectural decision changes
4. Update this README.md with change summary
5. Commit with descriptive message

## Related Files

### Project Root
- `README.md` - Project overview and setup instructions
- `requirements.txt` - Python dependencies
- `docker-compose.yml` - Docker configuration

### Source Code
- `src/` - Application source code
- `tests/` - Test suite
- `frontend/` - Streamlit frontend

### Data
- `data/models/` - Model storage (auto-created)

---

**Last Updated**: November 2, 2025  
**POC Status**: In Development (Session 3-4)  
**Documentation Version**: 1.1

