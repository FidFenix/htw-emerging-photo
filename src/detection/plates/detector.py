"""License plate detection using YOLO"""

from typing import List
import numpy as np
import torch
from ultralytics import YOLO

from src.detection.base import Detector, Detection, BoundingBox
from src.utils.exceptions import ModelLoadError, DetectionError
from src.utils.logger import get_logger


class PlateDetector(Detector):
    """Detects license plates using YOLO model"""
    
    def __init__(self, confidence_threshold: float = 0.6):
        """
        Initialize plate detector
        
        Args:
            confidence_threshold: Minimum confidence score for detections
        """
        self.confidence_threshold = confidence_threshold
        self.model = None
        self.logger = get_logger(self.__class__.__name__)
        self.load_model()
    
    def load_model(self) -> None:
        """Load YOLO model with GPU support"""
        try:
            self.logger.info("Loading YOLO model for license plate detection...")
            
            # Detect available device (CUDA GPU or CPU)
            if torch.cuda.is_available():
                self.device = 'cuda'
                self.logger.info(f"CUDA GPU detected: {torch.cuda.get_device_name(0)}")
            else:
                self.device = 'cpu'
                self.logger.info("No CUDA GPU detected, using CPU")
            
            # Using YOLOv8 nano model (lightweight for POC)
            # In production, use a model specifically trained on license plates
            self.model = YOLO('yolov8n.pt')
            self.model.to(self.device)
            
            self.logger.info(f"YOLO model loaded successfully on {self.device.upper()}")
        except Exception as e:
            self.logger.error(f"Failed to load YOLO model: {e}")
            raise ModelLoadError(f"Failed to load YOLO model: {str(e)}")
    
    def detect(self, image: np.ndarray) -> List[Detection]:
        """
        Detect license plates in image
        
        Args:
            image: Image as numpy array (RGB)
            
        Returns:
            List of Detection objects for license plates
        """
        if self.model is None:
            raise DetectionError("Model not loaded")
        
        try:
            self.logger.info(f"Running plate detection on image shape: {image.shape}")
            
            # Run detection with GPU device
            # For POC, we're using general object detection
            # In production, use a model trained specifically on license plates
            results = self.model(image, verbose=False, device=self.device)
            self.logger.info(f"YOLO returned {len(results)} result objects")
            
            detections = []
            detection_id = 1
            
            for result in results:
                boxes = result.boxes
                self.logger.info(f"Processing {len(boxes)} boxes from YOLO")
                
                for box in boxes:
                    try:
                        # Get confidence
                        confidence = float(box.conf[0])
                        
                        # Filter by confidence threshold
                        if confidence < self.confidence_threshold:
                            continue
                        
                        # Get class (for POC, we'll detect cars/vehicles as proxy for plates)
                        # Class 2 = car, 3 = motorcycle, 5 = bus, 7 = truck
                        cls = int(box.cls[0])
                        if cls not in [2, 3, 5, 7]:
                            continue
                        
                        # Get bounding box
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        
                        # Create detection
                        detection = Detection(
                            id=detection_id,
                            bbox=BoundingBox(
                                x=int(x1),
                                y=int(y1),
                                width=int(x2 - x1),
                                height=int(y2 - y1)
                            ),
                            confidence=confidence,
                            label="plate"
                        )
                        detections.append(detection)
                        detection_id += 1
                    except Exception as e:
                        self.logger.warning(f"Failed to process box: {e}")
                        continue
            
            self.logger.info(
                f"Detected {len(detections)} potential license plates "
                f"(threshold: {self.confidence_threshold})"
            )
            
            return detections
            
        except Exception as e:
            self.logger.error(f"License plate detection failed: {e}", exc_info=True)
            raise DetectionError(f"License plate detection failed: {str(e)}")

