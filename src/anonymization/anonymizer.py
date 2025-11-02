"""Image anonymization with yellow color fill"""

import base64
import io
from typing import List, Tuple
from PIL import Image, ImageDraw
import numpy as np

from src.detection.base import Detection
from src.utils.logger import get_logger


class Anonymizer:
    """Anonymizes images by filling detected regions with yellow color"""
    
    def __init__(self, color: str = "#FFFF00"):
        """
        Initialize anonymizer
        
        Args:
            color: Hex color code for anonymization (default: yellow #FFFF00)
        """
        self.color = color
        self.logger = get_logger(self.__class__.__name__)
    
    def anonymize(
        self,
        image: Image.Image,
        detections: List[Detection]
    ) -> Tuple[Image.Image, str]:
        """
        Anonymize image by filling detected regions with yellow color
        
        Args:
            image: PIL Image object
            detections: List of Detection objects (faces and plates)
            
        Returns:
            Tuple of (anonymized PIL Image, base64-encoded image string)
        """
        # Create a copy of the image
        anonymized_image = image.copy()
        draw = ImageDraw.Draw(anonymized_image)
        
        # Fill each detection with yellow color
        for detection in detections:
            bbox = detection.bbox
            x1 = bbox.x
            y1 = bbox.y
            x2 = bbox.x + bbox.width
            y2 = bbox.y + bbox.height
            
            # Draw filled rectangle
            draw.rectangle(
                [(x1, y1), (x2, y2)],
                fill=self.color,
                outline=self.color
            )
            
            self.logger.info(
                f"Anonymized {detection.label} {detection.id} at "
                f"({x1}, {y1}, {x2}, {y2}) size: {bbox.width}x{bbox.height} with {self.color}"
            )
        
        self.logger.info(
            f"Anonymized {len(detections)} regions with color {self.color}"
        )
        
        # Encode to base64
        base64_image = self._encode_image(anonymized_image)
        
        return anonymized_image, base64_image
    
    def _encode_image(self, image: Image.Image) -> str:
        """
        Encode PIL Image to base64 string
        
        Args:
            image: PIL Image object
            
        Returns:
            Base64-encoded image string
        """
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        buffer.seek(0)
        base64_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return base64_str

