"""Detection module for faces and license plates"""

from .base import Detection, BoundingBox, Detector
from .faces.detector import FaceDetector
from .plates.detector import PlateDetector

__all__ = [
    "Detection",
    "BoundingBox",
    "Detector",
    "FaceDetector",
    "PlateDetector",
]

