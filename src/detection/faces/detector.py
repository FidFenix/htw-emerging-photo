"""Face detection using RetinaFace"""

from typing import List
import numpy as np
from insightface.app import FaceAnalysis

from src.detection.base import Detector, Detection, BoundingBox
from src.utils.exceptions import ModelLoadError, DetectionError
from src.utils.logger import get_logger


class FaceDetector(Detector):
    """Detects faces using RetinaFace model"""
    
    def __init__(self, confidence_threshold: float = 0.7):
        """
        Initialize face detector
        
        Args:
            confidence_threshold: Minimum confidence score for detections
        """
        self.confidence_threshold = confidence_threshold
        self.model = None
        self.logger = get_logger(self.__class__.__name__)
        self.load_model()
    
    def load_model(self) -> None:
        """Load RetinaFace model with GPU support (MPS for Apple Silicon)"""
        try:
            self.logger.info("Loading RetinaFace model with GPU support...")
            
            # Try to use GPU (CUDA or fallback to CPU)
            # Note: InsightFace uses ONNX Runtime which doesn't support MPS directly
            # We'll use CUDA if available, otherwise CPU
            try:
                self.model = FaceAnalysis(
                    name='buffalo_l',
                    providers=['CUDAExecutionProvider', 'CPUExecutionProvider']
                )
                self.model.prepare(ctx_id=0, det_size=(640, 640))
                self.logger.info("RetinaFace model loaded successfully on CUDA GPU")
            except Exception as gpu_error:
                self.logger.warning(f"CUDA not available: {gpu_error}")
                self.logger.info("Using CPU for RetinaFace (ONNX Runtime doesn't support MPS)")
                self.model = FaceAnalysis(
                    name='buffalo_l',
                    providers=['CPUExecutionProvider']
                )
                self.model.prepare(ctx_id=-1, det_size=(640, 640))
                self.logger.info("RetinaFace model loaded successfully on CPU")
                
        except Exception as e:
            self.logger.error(f"Failed to load RetinaFace model: {e}")
            raise ModelLoadError(f"Failed to load RetinaFace model: {str(e)}")
    
    def detect(self, image: np.ndarray) -> List[Detection]:
        """
        Detect faces in image
        
        Args:
            image: Image as numpy array (RGB)
            
        Returns:
            List of Detection objects for faces
        """
        if self.model is None:
            raise DetectionError("Model not loaded")
        
        try:
            self.logger.info(f"Running face detection on image shape: {image.shape}")
            
            # Ensure image is in correct format (RGB, uint8)
            if image.dtype != np.uint8:
                image = (image * 255).astype(np.uint8) if image.max() <= 1.0 else image.astype(np.uint8)
            
            # Run detection
            faces = self.model.get(image)
            self.logger.info(f"RetinaFace returned {len(faces)} raw detections")
            
            detections = []
            for idx, face in enumerate(faces):
                try:
                    # Get bounding box
                    bbox = face.bbox.astype(int)
                    x, y, x2, y2 = bbox
                    
                    # Get confidence
                    confidence = float(face.det_score)
                    
                    # Filter by confidence threshold
                    if confidence < self.confidence_threshold:
                        continue
                    
                    # Create detection
                    detection = Detection(
                        id=idx + 1,
                        bbox=BoundingBox(
                            x=int(x),
                            y=int(y),
                            width=int(x2 - x),
                            height=int(y2 - y)
                        ),
                        confidence=confidence,
                        label="face"
                    )
                    detections.append(detection)
                except Exception as e:
                    self.logger.warning(f"Failed to process face {idx}: {e}")
                    continue
            
            self.logger.info(
                f"Detected {len(detections)} faces "
                f"(threshold: {self.confidence_threshold})"
            )
            
            return detections
            
        except Exception as e:
            self.logger.error(f"Face detection failed: {e}", exc_info=True)
            raise DetectionError(f"Face detection failed: {str(e)}")

