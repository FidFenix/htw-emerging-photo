"""Anonymization API endpoints"""

import time
from typing import Dict, Any
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse

from src.config import get_settings
from src.preprocessing import ImageValidator, ImagePreprocessor
from src.detection import FaceDetector, PlateDetector
from src.anonymization import Anonymizer, ResultFormatter
from src.utils.exceptions import InvalidImageError, DetectionError
from src.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

# Initialize components (singleton pattern for POC)
settings = get_settings()
face_detector = None
plate_detector = None
anonymizer = None
preprocessor = None


def get_components():
    """Lazy initialization of detection components"""
    global face_detector, plate_detector, anonymizer, preprocessor
    
    if face_detector is None:
        logger.info("Initializing face detector...")
        face_detector = FaceDetector(
            confidence_threshold=settings.face_confidence_threshold
        )
    
    if plate_detector is None and settings.enable_plate_detection:
        logger.info("Initializing plate detector...")
        plate_detector = PlateDetector(
            confidence_threshold=settings.plate_confidence_threshold
        )
    
    if anonymizer is None:
        logger.info("Initializing anonymizer...")
        anonymizer = Anonymizer(color=settings.anonymization_color)
    
    if preprocessor is None:
        preprocessor = ImagePreprocessor()
    
    return face_detector, plate_detector, anonymizer, preprocessor


@router.post("/anonymize", response_model=Dict[str, Any])
async def anonymize_image(
    file: UploadFile = File(..., description="Image file (JPG/PNG, max 10MB)")
) -> JSONResponse:
    """
    Anonymize faces and license plates in uploaded image
    
    This endpoint:
    1. Validates the uploaded image (format, size, integrity)
    2. Preprocesses the image (resize, normalize)
    3. Detects faces using RetinaFace
    4. Detects license plates using YOLO
    5. Anonymizes detected regions with yellow color (#FFFF00)
    6. Returns anonymized image and detection metadata
    
    Args:
        file: Uploaded image file (JPG or PNG format, max 10MB)
        
    Returns:
        JSON response with:
        - success: Boolean indicating success
        - processing_time: Time taken in seconds
        - anonymized_image: Base64-encoded anonymized image
        - faces_anonymized: List of anonymized face regions
        - plates_anonymized: List of anonymized plate regions
        - summary: Summary statistics
        
    Raises:
        HTTPException: If validation or processing fails
    """
    start_time = time.time()
    
    try:
        # Read file
        image_bytes = await file.read()
        logger.info(f"Received file: {file.filename}, size: {len(image_bytes)} bytes")
        
        # Validate image
        try:
            image = ImageValidator.validate_image(
                image_bytes,
                max_size=settings.max_upload_size
            )
        except InvalidImageError as e:
            logger.warning(f"Image validation failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        
        # Check file size explicitly for 413 error
        if len(image_bytes) > settings.max_upload_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds maximum allowed size of 10MB"
            )
        
        # Get components
        face_det, plate_det, anon, preproc = get_components()
        
        # Preprocess image
        image_array, processed_image = preproc.preprocess(image)
        
        # Detect faces
        logger.info("Running face detection...")
        face_detections = face_det.detect(image_array)
        
        # Detect license plates (only if enabled)
        plate_detections = []
        if settings.enable_plate_detection:
            logger.info("Running license plate detection...")
            try:
                plate_detections = plate_det.detect(image_array)
            except Exception as e:
                logger.warning(f"License plate detection failed: {e}")
                logger.info("Continuing with face detection only")
        else:
            logger.info("License plate detection is disabled (enable_plate_detection=False)")
        
        # Combine all detections
        all_detections = face_detections + plate_detections
        logger.info(
            f"Total detections: {len(all_detections)} "
            f"(faces: {len(face_detections)}, plates: {len(plate_detections)})"
        )
        
        # Anonymize image
        logger.info("Anonymizing image...")
        anonymized_image, base64_image = anon.anonymize(
            processed_image,
            all_detections
        )
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Format response
        response = ResultFormatter.format_response(
            success=True,
            processing_time=processing_time,
            anonymized_image=base64_image,
            face_detections=face_detections,
            plate_detections=plate_detections,
            anonymization_color=settings.anonymization_color
        )
        
        logger.info(
            f"Anonymization completed in {processing_time:.2f}s: "
            f"{len(face_detections)} faces, {len(plate_detections)} plates"
        )
        
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
        
    except HTTPException:
        raise
    except DetectionError as e:
        logger.error(f"Detection error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Detection failed: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/info")
async def get_info() -> Dict[str, Any]:
    """
    Get API information and configuration
    
    Returns:
        API configuration details
    """
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "models": {
            "face_detection": settings.face_detection_model,
            "plate_detection": settings.plate_detection_model if settings.enable_plate_detection else "disabled"
        },
        "thresholds": {
            "face_confidence": settings.face_confidence_threshold,
            "plate_confidence": settings.plate_confidence_threshold if settings.enable_plate_detection else "N/A"
        },
        "anonymization": {
            "color": settings.anonymization_color,
            "method": "solid_fill"
        },
        "limits": {
            "max_upload_size_mb": settings.max_upload_size / (1024 * 1024),
            "supported_formats": ["JPG", "PNG"]
        },
        "features": {
            "face_detection": True,
            "plate_detection": settings.enable_plate_detection
        }
    }

