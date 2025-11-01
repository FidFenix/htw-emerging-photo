"""Image validation utilities"""

import io
from typing import Tuple
from PIL import Image
from src.utils.exceptions import InvalidImageError
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ImageValidator:
    """Validates uploaded images"""
    
    ALLOWED_FORMATS = {"JPEG", "PNG"}
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
    MAX_DIMENSION = 4096
    
    @staticmethod
    def validate_file_size(file_size: int, max_size: int) -> None:
        """
        Validate file size
        
        Args:
            file_size: Size of file in bytes
            max_size: Maximum allowed size in bytes
            
        Raises:
            InvalidImageError: If file size exceeds maximum
        """
        if file_size > max_size:
            raise InvalidImageError(
                f"File size {file_size} bytes exceeds maximum {max_size} bytes (10MB)"
            )
    
    @staticmethod
    def validate_format(image: Image.Image) -> None:
        """
        Validate image format
        
        Args:
            image: PIL Image object
            
        Raises:
            InvalidImageError: If format is not supported
        """
        if image.format not in ImageValidator.ALLOWED_FORMATS:
            raise InvalidImageError(
                f"Unsupported format: {image.format}. "
                f"Allowed formats: {', '.join(ImageValidator.ALLOWED_FORMATS)}"
            )
    
    @staticmethod
    def validate_image(image_bytes: bytes, max_size: int) -> Image.Image:
        """
        Validate image bytes and return PIL Image
        
        Args:
            image_bytes: Raw image bytes
            max_size: Maximum file size in bytes
            
        Returns:
            Validated PIL Image object
            
        Raises:
            InvalidImageError: If validation fails
        """
        # Check file size
        ImageValidator.validate_file_size(len(image_bytes), max_size)
        
        # Try to open image
        try:
            image = Image.open(io.BytesIO(image_bytes))
            image.verify()  # Verify it's a valid image
            
            # Reopen after verify (verify closes the file)
            image = Image.open(io.BytesIO(image_bytes))
            
        except Exception as e:
            logger.error(f"Failed to open image: {e}")
            raise InvalidImageError(f"Invalid or corrupted image file: {str(e)}")
        
        # Validate format
        ImageValidator.validate_format(image)
        
        logger.info(
            f"Image validated: format={image.format}, "
            f"size={image.size}, mode={image.mode}"
        )
        
        return image

