"""Custom exceptions for the application"""


class AnonymizationError(Exception):
    """Base exception for anonymization errors"""
    pass


class InvalidImageError(AnonymizationError):
    """Raised when image validation fails"""
    pass


class ModelLoadError(AnonymizationError):
    """Raised when model loading fails"""
    pass


class DetectionError(AnonymizationError):
    """Raised when detection fails"""
    pass

