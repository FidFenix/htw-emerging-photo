"""Base classes for detection"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
import numpy as np


@dataclass
class BoundingBox:
    """Bounding box coordinates"""
    x: int
    y: int
    width: int
    height: int
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height
        }


@dataclass
class Detection:
    """Represents a single detection"""
    id: int
    bbox: BoundingBox
    confidence: float
    label: str  # "face" or "plate"
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "bbox": self.bbox.to_dict(),
            "confidence": float(self.confidence),
            "label": self.label
        }


class Detector(ABC):
    """Base interface for all detectors"""
    
    @abstractmethod
    def detect(self, image: np.ndarray) -> List[Detection]:
        """
        Detect objects in image
        
        Args:
            image: Image as numpy array (RGB)
            
        Returns:
            List of Detection objects
        """
        pass
    
    @abstractmethod
    def load_model(self) -> None:
        """Load detection model"""
        pass

