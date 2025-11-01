"""Image preprocessing for detection models"""

import numpy as np
from PIL import Image
from typing import Tuple
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ImagePreprocessor:
    """Preprocesses images for detection models"""
    
    MAX_DIMENSION = 4096
    
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
    
    def preprocess(self, image: Image.Image) -> Tuple[np.ndarray, Image.Image]:
        """
        Preprocess image for detection
        
        Args:
            image: PIL Image object
            
        Returns:
            Tuple of (numpy array for detection, processed PIL Image)
        """
        # Convert to RGB if needed
        if image.mode != 'RGB':
            self.logger.info(f"Converting image from {image.mode} to RGB")
            image = image.convert('RGB')
        
        # Resize if too large
        if max(image.size) > self.MAX_DIMENSION:
            self.logger.info(
                f"Resizing image from {image.size} "
                f"(max dimension > {self.MAX_DIMENSION})"
            )
            image = self._resize_image(image)
        
        # Convert to numpy array
        image_array = np.array(image)
        
        self.logger.info(
            f"Preprocessed image: shape={image_array.shape}, "
            f"dtype={image_array.dtype}"
        )
        
        return image_array, image
    
    def _resize_image(self, image: Image.Image) -> Image.Image:
        """
        Resize image while maintaining aspect ratio
        
        Args:
            image: PIL Image object
            
        Returns:
            Resized PIL Image
        """
        width, height = image.size
        
        if width > height:
            new_width = self.MAX_DIMENSION
            new_height = int(height * (self.MAX_DIMENSION / width))
        else:
            new_height = self.MAX_DIMENSION
            new_width = int(width * (self.MAX_DIMENSION / height))
        
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

