"""Format anonymization results for API response"""

from typing import List, Dict, Any
from src.detection.base import Detection


class ResultFormatter:
    """Formats anonymization results into structured JSON response"""
    
    @staticmethod
    def format_response(
        success: bool,
        processing_time: float,
        anonymized_image: str,
        face_detections: List[Detection],
        plate_detections: List[Detection],
        anonymization_color: str,
        error_message: str = None
    ) -> Dict[str, Any]:
        """
        Format anonymization results into JSON response
        
        Args:
            success: Whether anonymization was successful
            processing_time: Time taken for processing in seconds
            anonymized_image: Base64-encoded anonymized image
            face_detections: List of face Detection objects
            plate_detections: List of plate Detection objects
            anonymization_color: Hex color used for anonymization
            error_message: Optional error message if success=False
            
        Returns:
            Formatted response dictionary
        """
        if not success:
            return {
                "success": False,
                "error": error_message or "Anonymization failed",
                "processing_time": processing_time
            }
        
        # Format face detections
        faces_anonymized = [
            {
                "id": det.id,
                "bbox": det.bbox.to_dict(),
                "confidence": round(det.confidence, 2),
                "anonymization_color": anonymization_color
            }
            for det in face_detections
        ]
        
        # Format plate detections
        plates_anonymized = [
            {
                "id": det.id,
                "bbox": det.bbox.to_dict(),
                "confidence": round(det.confidence, 2),
                "anonymization_color": anonymization_color
            }
            for det in plate_detections
        ]
        
        return {
            "success": True,
            "processing_time": round(processing_time, 2),
            "anonymized_image": anonymized_image,
            "faces_anonymized": faces_anonymized,
            "plates_anonymized": plates_anonymized,
            "summary": {
                "total_faces": len(face_detections),
                "total_plates": len(plate_detections),
                "total_anonymized": len(face_detections) + len(plate_detections),
                "anonymization_color": anonymization_color
            }
        }
    
    @staticmethod
    def format_error(error_message: str, status_code: int = 400) -> Dict[str, Any]:
        """
        Format error response
        
        Args:
            error_message: Error message
            status_code: HTTP status code
            
        Returns:
            Formatted error response
        """
        return {
            "success": False,
            "error": error_message,
            "status_code": status_code
        }

