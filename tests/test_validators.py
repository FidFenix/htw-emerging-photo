"""Tests for image validators"""

import pytest
from PIL import Image
import io

from src.preprocessing.validators import ImageValidator
from src.utils.exceptions import InvalidImageError


def create_test_image(format="PNG", size=(100, 100)):
    """Create a test image"""
    img = Image.new('RGB', size, color='red')
    buffer = io.BytesIO()
    img.save(buffer, format=format)
    buffer.seek(0)
    return buffer.getvalue()


def test_validate_file_size_valid():
    """Test file size validation with valid size"""
    ImageValidator.validate_file_size(1000, 10000)  # Should not raise


def test_validate_file_size_invalid():
    """Test file size validation with invalid size"""
    with pytest.raises(InvalidImageError):
        ImageValidator.validate_file_size(11000, 10000)


def test_validate_format_valid():
    """Test format validation with valid format"""
    img = Image.new('RGB', (100, 100))
    img.format = 'PNG'
    ImageValidator.validate_format(img)  # Should not raise


def test_validate_format_invalid():
    """Test format validation with invalid format"""
    img = Image.new('RGB', (100, 100))
    img.format = 'BMP'
    with pytest.raises(InvalidImageError):
        ImageValidator.validate_format(img)


def test_validate_image_valid_png():
    """Test image validation with valid PNG"""
    image_bytes = create_test_image(format="PNG")
    img = ImageValidator.validate_image(image_bytes, max_size=10485760)
    assert img.format == "PNG"


def test_validate_image_valid_jpeg():
    """Test image validation with valid JPEG"""
    image_bytes = create_test_image(format="JPEG")
    img = ImageValidator.validate_image(image_bytes, max_size=10485760)
    assert img.format == "JPEG"


def test_validate_image_too_large():
    """Test image validation with oversized file"""
    image_bytes = create_test_image(format="PNG")
    with pytest.raises(InvalidImageError):
        ImageValidator.validate_image(image_bytes, max_size=100)


def test_validate_image_corrupted():
    """Test image validation with corrupted data"""
    corrupted_bytes = b"not an image"
    with pytest.raises(InvalidImageError):
        ImageValidator.validate_image(corrupted_bytes, max_size=10485760)

