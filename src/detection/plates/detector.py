"""License plate detection using YOLO and OCR fallback"""

from typing import List, Optional
import numpy as np
import torch
import cv2
from ultralytics import YOLO
from scipy.signal import find_peaks
from pathlib import Path
from huggingface_hub import hf_hub_download, list_repo_files

from src.detection.base import Detector, Detection, BoundingBox
from src.utils.exceptions import ModelLoadError, DetectionError
from src.utils.logger import get_logger


class PlateDetector(Detector):
    """Detects license plates using YOLO model"""
    
    def __init__(self, confidence_threshold: float = 0.25):
        """
        Initialize plate detector
        
        Args:
            confidence_threshold: Minimum confidence score for detections
        """
        self.confidence_threshold = confidence_threshold
        self.model = None
        self.use_two_stage_detection = True  # Always use two-stage with YOLOv8n
        self.logger = get_logger(self.__class__.__name__)
        self.load_model()
    
    def load_model(self) -> None:
        """Load YOLO model with GPU support (MPS for Apple Silicon, CUDA for NVIDIA)"""
        try:
            self.logger.info("Loading YOLO model for license plate detection...")
            
            # Detect available device: MPS (Apple Silicon) > CUDA (NVIDIA) > CPU
            if torch.backends.mps.is_available():
                self.device = 'mps'
                self.logger.info("MPS (Apple Silicon GPU) detected")
            elif torch.cuda.is_available():
                self.device = 'cuda'
                self.logger.info(f"CUDA GPU detected: {torch.cuda.get_device_name(0)}")
            else:
                self.device = 'cpu'
                self.logger.info("No GPU detected, using CPU")
            
            # Using YOLOv8 for license plate detection
            self.logger.info("Loading YOLOv8 model for license plate detection...")
            
            # Try to load a license plate specific model
            models_dir = Path('data/models')
            models_dir.mkdir(parents=True, exist_ok=True)
            
            local_model = models_dir / 'license_plate_detector.pt'
            
            if local_model.exists() and local_model.stat().st_size > 1000000:  # > 1MB (not HTML)
                self.logger.info(f"✅ Loading custom license plate model: {local_model}")
                self.model = YOLO(str(local_model))
                self._is_custom_model = True
                self.use_two_stage_detection = False  # Trust the custom model
                self.logger.info("✅ Custom license plate model loaded - will detect plates directly")
            else:
                # Try to load YOLOv11 license plate model from Hugging Face
                self.logger.info("No custom model found. Trying to download from Hugging Face...")
                
                repo_id = "morsetechlab/yolov11-license-plate-detection"
                self.logger.info(f"Trying repository: {repo_id}...")
                
                loaded_model = self._load_model_from_huggingface(repo_id)
                
                if loaded_model is not None:
                    self.model = loaded_model
                    self._is_custom_model = True
                    self.use_two_stage_detection = False
                    self.logger.info(f"✅ License plate model loaded from Hugging Face: {repo_id}")
                else:
                    # If Hugging Face download failed, use YOLOv8n with two-stage detection
                    self.logger.warning(f"Failed to load model from {repo_id}")
                    self.logger.info("=" * 80)
                    self.logger.info("Using YOLOv8n with two-stage detection (car → plate)")
                    self.logger.info("This fallback method works but may have lower accuracy.")
                    self.logger.info("")
                    self.logger.info("💡 To use a specialized license plate model:")
                    self.logger.info(f"  Option 1: Download from Roboflow Universe")
                    self.logger.info(f"    - Visit: https://universe.roboflow.com/")
                    self.logger.info(f"    - Search: 'license plate detection yolov8'")
                    self.logger.info(f"    - Download YOLOv8 model (best.pt)")
                    self.logger.info(f"    - Save as: {local_model}")
                    self.logger.info(f"    - Restart backend")
                    self.logger.info("")
                    self.logger.info(f"  Option 2: The current two-stage detection should work")
                    self.logger.info(f"    - Detects vehicles first, then finds plates within them")
                    self.logger.info(f"    - Test it with an image containing a license plate")
                    self.logger.info("")
                    self.logger.info("=" * 80)
                    self.model = YOLO('yolov8n.pt')
                    self._is_custom_model = False
                    self.use_two_stage_detection = True
            
            self.model.to(self.device)
            self.logger.info(f"YOLO model loaded successfully on {self.device.upper()}")
        except Exception as e:
            self.logger.error(f"Failed to load YOLO model: {e}")
            raise ModelLoadError(f"Failed to load YOLO model: {str(e)}")
    
    def _load_model_from_huggingface(self, repo_id: str) -> Optional[YOLO]:
        """
        Load YOLO model from Hugging Face Hub
        Downloads specific model file: license-plate-finetune-v1l.pt
        
        Args:
            repo_id: Hugging Face repository ID (e.g., "username/model-name")
            
        Returns:
            YOLO model if successful, None otherwise
        """
        self.logger.info(f"📥 Loading model from {repo_id}")
        
        # Download specific model file using hf_hub_download
        try:
            self.logger.info("Listing available files in repository...")
            
            files = list_repo_files(repo_id)
            pt_files = [f for f in files if f.endswith('.pt')]
            
            self.logger.info(f"Found {len(pt_files)} .pt model file(s): {pt_files}")
            
            if pt_files:
                # Use the first .pt file found
                filename = pt_files[0]
                self.logger.info(f"✅ Using model file: {filename}")
                
                self.logger.info(f"Downloading {filename} from {repo_id}...")
                
                model_file = hf_hub_download(
                    repo_id=repo_id,
                    filename=filename
                )
                
                self.logger.info(f"Model downloaded to: {model_file}")
                self.logger.info(f"Loading YOLO model from downloaded file...")
                
                model = YOLO(model_file)
                self.logger.info(f"✅ Model loaded successfully from {filename}!")
                return model
            else:
                self.logger.error("No .pt model files found in repository")
                self.logger.info(f"Available files: {files[:10]}...")  # Show first 10 files
                return None
                
        except Exception as e:
            self.logger.error(f"Failed to load model: {str(e)}")
            import traceback
            self.logger.debug(f"Traceback: {traceback.format_exc()}")
            return None
    
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
            
            # Check if we have a custom license plate model
            has_custom_model = hasattr(self, '_is_custom_model') and self._is_custom_model
            
            for result in results:
                boxes = result.boxes
                self.logger.info(f"Processing {len(boxes)} boxes from YOLO")
                
                for box in boxes:
                    try:
                        # Get confidence
                        confidence = float(box.conf[0])
                        
                        self.logger.info(f"Box detected with confidence: {confidence:.3f} (threshold: {self.confidence_threshold})")
                        
                        # Filter by confidence threshold
                        if confidence < self.confidence_threshold:
                            self.logger.info(f"  → Skipped: confidence {confidence:.3f} < threshold {self.confidence_threshold}")
                            continue
                        
                        # Get bounding box
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        
                        # Ensure valid coordinates
                        x1, x2 = min(x1, x2), max(x1, x2)
                        y1, y2 = min(y1, y2), max(y1, y2)
                        
                        width = int(x2 - x1)
                        height = int(y2 - y1)
                        
                        # Skip invalid boxes
                        if width <= 0 or height <= 0:
                            self.logger.warning(f"  → Skipped: invalid box dimensions {width}x{height}")
                            continue
                        
                        aspect_ratio = width / height if height > 0 else 0
                        
                        self.logger.info(f"  → Box: ({int(x1)}, {int(y1)}, {int(x2)}, {int(y2)}), size: {width}x{height}, aspect: {aspect_ratio:.2f}")
                        
                        # For custom license plate models, trust the model completely
                        if has_custom_model:
                            # No validation - trust the specialized model
                            self.logger.info(f"  → Using custom model: accepting all detections above confidence threshold")
                        else:
                            # More strict validation for general models
                            if width < 10 or height < 5:
                                self.logger.info(f"  → Skipped: too small {width}x{height}")
                                continue
                            
                            # Very lenient aspect ratio check
                            if aspect_ratio < 1.0 or aspect_ratio > 10.0:
                                self.logger.info(f"  → Skipped: extreme aspect_ratio={aspect_ratio:.2f}")
                                continue
                        
                        self.logger.info(
                            f"✅ License plate accepted: {width}x{height}, "
                            f"aspect={aspect_ratio:.2f}, conf={confidence:.2f}"
                        )
                        
                        # Expand LEFT from top-right corner (double width)
                        expanded_width = int(width * 2.0)   # Double the width
                        x2_final = int(x2)  # Right edge stays
                        x1_final = max(0, x2_final - expanded_width)  # Expand left
                        
                        # Keep original height (no y-axis padding)
                        y1_final = int(y1)
                        y2_final = int(y2)
                        
                        # Ensure coordinates are valid
                        x1_final = max(0, x1_final)
                        y1_final = max(0, y1_final)
                        
                        width_final = x2_final - x1_final
                        height_final = y2_final - y1_final
                        
                        # Final validation
                        if width_final <= 0 or height_final <= 0:
                            self.logger.warning(f"  → Skipped: invalid final dimensions {width_final}x{height_final}")
                            continue
                        
                        self.logger.info(
                            f"  → Expanded 2x left: ({x1_final}, {y1_final}, {x2_final}, {y2_final}), "
                            f"size: {width_final}x{height_final} (original: {width}x{height})"
                        )
                        
                        # Create detection with expanded bbox from top-left corner
                        detection = Detection(
                            id=detection_id,
                            bbox=BoundingBox(
                                x=x1_final,
                                y=y1_final,
                                width=width_final,
                                height=height_final
                            ),
                            confidence=confidence,
                            label="plate"
                        )
                        detections.append(detection)
                        detection_id += 1
                    except Exception as e:
                        self.logger.warning(f"Failed to process box: {e}")
                        continue
            
            if len(detections) > 0:
                self.logger.info(
                    f"✅ YOLO detected {len(detections)} license plates "
                    f"(threshold: {self.confidence_threshold})"
                )
            else:
                self.logger.warning(
                    f"⚠️ YOLO found 0 license plates. "
                    f"Model: {self._is_custom_model if hasattr(self, '_is_custom_model') else 'unknown'}, "
                    f"Total boxes: {sum(len(r.boxes) for r in results)}"
                )
                
                # If YOLO didn't find any plates, use two-stage detection as fallback
                if self.use_two_stage_detection:
                    self.logger.info("No plates detected by primary model. Trying two-stage detection (car → plate)...")
                    two_stage_detections = self._detect_plates_two_stage(image, results)
                    detections.extend(two_stage_detections)
                else:
                    self.logger.info("No plates detected. Troubleshooting tips:")
                    self.logger.info("  1. Ensure image has visible license plates")
                    self.logger.info("  2. Check confidence threshold (current: {})".format(self.confidence_threshold))
                    self.logger.info("  3. Verify model is appropriate for your plate type (US/EU/Asian)")
            
            return detections
            
        except Exception as e:
            self.logger.error(f"License plate detection failed: {e}", exc_info=True)
            raise DetectionError(f"License plate detection failed: {str(e)}")
    
    def _detect_plates_with_contours(self, image: np.ndarray) -> List[Detection]:
        """
        Fallback method: Detect license plates using contour detection
        Works well for European plates with clear rectangular shapes
        """
        self.logger.info("Using contour-based detection for license plates...")
        
        detections = []
        detection_id = 1
        
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            
            # Apply bilateral filter to reduce noise while keeping edges sharp
            gray = cv2.bilateralFilter(gray, 11, 17, 17)
            
            # Apply adaptive thresholding to enhance text regions (typical for plates)
            thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                          cv2.THRESH_BINARY, 11, 2)
            
            # Edge detection with stricter parameters
            edges = cv2.Canny(gray, 50, 150)
            
            # Dilate edges to connect broken lines
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            dilated = cv2.dilate(edges, kernel, iterations=1)
            
            # Find contours
            contours, _ = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Sort contours by area (largest first)
            contours = sorted(contours, key=cv2.contourArea, reverse=True)[:20]
            
            image_area = image.shape[0] * image.shape[1]
            image_height, image_width = image.shape[:2]
            
            candidates = []
            
            for contour in contours:
                # Get bounding rectangle
                x, y, w, h = cv2.boundingRect(contour)
                
                # Calculate aspect ratio
                aspect_ratio = w / h if h > 0 else 0
                
                # Calculate relative size
                box_area = w * h
                relative_size = box_area / image_area if image_area > 0 else 0
                
                # Balanced European license plate characteristics:
                # - Aspect ratio: 1.8:1 to 6.0:1 (European plates vary)
                # - Size: 0.3% to 12% of image
                # - Minimum dimensions: 50x18 pixels
                # - Maximum dimensions: not more than 50% of image width/height
                
                if not (1.8 <= aspect_ratio <= 6.0):
                    self.logger.debug(f"Rejected: aspect_ratio={aspect_ratio:.2f}")
                    continue
                
                if not (0.003 <= relative_size <= 0.12):
                    self.logger.debug(f"Rejected: relative_size={relative_size:.4f}")
                    continue
                
                if w < 50 or h < 18:
                    self.logger.debug(f"Rejected: too small {w}x{h}")
                    continue
                
                if w > image_width * 0.5 or h > image_height * 0.5:
                    self.logger.debug(f"Rejected: too large {w}x{h}")
                    continue
                
                # Check rectangularity (should be mostly rectangular)
                rect_area = w * h
                contour_area = cv2.contourArea(contour)
                extent = 0.8  # Default if calculation fails
                if contour_area > 0:
                    extent = rect_area / contour_area
                    if extent < 0.65:  # Should be at least 65% rectangular
                        self.logger.debug(f"Rejected: extent={extent:.2f}")
                        continue
                
                # Extract ROI and check for text-like patterns (plates have text)
                edge_density = 0.1  # Default
                horizontal_variance = 1000  # Default (pass)
                
                roi = gray[y:y+h, x:x+w]
                if roi.size > 0:
                    # Check edge density (plates have lots of edges from text)
                    roi_edges = cv2.Canny(roi, 30, 150)
                    edge_density = np.sum(roi_edges > 0) / roi.size
                    
                    # License plates typically have 3-30% edge density (more lenient)
                    if not (0.03 <= edge_density <= 0.35):
                        self.logger.debug(f"Rejected: edge_density={edge_density:.3f}")
                        continue
                    
                    # Check for horizontal text patterns (most plates have horizontal text)
                    horizontal_edges = np.sum(roi_edges, axis=1)
                    if len(horizontal_edges) > 0:
                        horizontal_variance = np.var(horizontal_edges)
                        # More lenient variance check
                        if horizontal_variance < 50:
                            self.logger.debug(f"Rejected: horizontal_variance={horizontal_variance:.1f}")
                            continue
                
                # Store candidate with score
                # Boost score for typical plate characteristics
                aspect_score = 1.0
                if 2.0 <= aspect_ratio <= 5.0:  # Typical European plate
                    aspect_score = 1.5
                
                score = aspect_ratio * edge_density * extent * aspect_score
                candidates.append((score, x, y, w, h, aspect_ratio, relative_size, edge_density))
            
            # Sort by score and take top 5 candidates
            candidates.sort(reverse=True, key=lambda x: x[0])
            
            for score, x, y, w, h, aspect_ratio, relative_size, edge_density in candidates[:5]:
                # Create detection
                detection = Detection(
                    id=detection_id,
                    bbox=BoundingBox(
                        x=int(x),
                        y=int(y),
                        width=int(w),
                        height=int(h)
                    ),
                    confidence=min(0.95, 0.7 + (score / 10)),  # Variable confidence based on score
                    label="plate"
                )
                detections.append(detection)
                self.logger.info(
                    f"Contour-based plate {detection_id}: "
                    f"{w}x{h}, aspect={aspect_ratio:.2f}, size={relative_size:.4f}, "
                    f"edge_density={edge_density:.3f}, score={score:.3f}"
                )
                detection_id += 1
            
            self.logger.info(f"Contour-based detection found {len(detections)} potential plates")
            return detections
            
        except Exception as e:
            self.logger.warning(f"Contour-based detection failed: {e}")
            return []
    
    def _detect_plates_two_stage(self, image: np.ndarray, yolo_results) -> List[Detection]:
        """
        Two-stage detection: First find cars, then find license plates within car regions
        This is more reliable as it narrows down the search space
        """
        self.logger.info("Using two-stage detection: car → license plate...")
        
        detections = []
        detection_id = 1
        
        try:
            # Step 1: Find all vehicles (cars, trucks, buses, motorcycles)
            vehicle_classes = [2, 3, 5, 7]  # car, motorcycle, bus, truck
            vehicle_regions = []
            
            for result in yolo_results:
                boxes = result.boxes
                for box in boxes:
                    cls = int(box.cls[0])
                    confidence = float(box.conf[0])
                    
                    # Check if it's a vehicle with reasonable confidence
                    if cls in vehicle_classes and confidence > 0.4:
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        vehicle_regions.append((int(x1), int(y1), int(x2), int(y2)))
                        self.logger.info(f"Found vehicle: {int(x1)},{int(y1)} to {int(x2)},{int(y2)}")
            
            if len(vehicle_regions) == 0:
                self.logger.info("No vehicles detected, cannot use two-stage detection")
                return []
            
            self.logger.info(f"Found {len(vehicle_regions)} vehicles, searching for plates within them...")
            
            # Step 2: For each vehicle, search for license plate using contour detection
            for vehicle_idx, (vx1, vy1, vx2, vy2) in enumerate(vehicle_regions):
                # Extract vehicle ROI
                vehicle_roi = image[vy1:vy2, vx1:vx2]
                
                if vehicle_roi.size == 0:
                    continue
                
                self.logger.info(f"Searching in vehicle {vehicle_idx + 1}: {vx2-vx1}x{vy2-vy1}")
                
                # Find plates within this vehicle
                plate_detections = self._find_plates_in_region(vehicle_roi, vx1, vy1)
                
                for plate_det in plate_detections:
                    # Adjust detection ID
                    plate_det.id = detection_id
                    detections.append(plate_det)
                    self.logger.info(
                        f"Found plate {detection_id} in vehicle {vehicle_idx + 1}: "
                        f"{plate_det.bbox.width}x{plate_det.bbox.height}"
                    )
                    detection_id += 1
            
            self.logger.info(f"Two-stage detection found {len(detections)} license plates")
            return detections
            
        except Exception as e:
            self.logger.warning(f"Two-stage detection failed: {e}")
            return []
    
    def _find_plates_in_region(self, roi: np.ndarray, offset_x: int, offset_y: int) -> List[Detection]:
        """
        Find license plates within a specific region (typically a vehicle)
        Uses multiple detection techniques with very lenient criteria
        """
        detections = []
        
        try:
            roi_height, roi_width = roi.shape[:2]
            roi_area = roi_width * roi_height
            
            self.logger.info(f"Analyzing vehicle region: {roi_width}x{roi_height}")
            
            # Convert to grayscale
            gray = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY)
            
            # Try multiple preprocessing techniques
            # Method 1: Bilateral filter + Canny
            gray_filtered = cv2.bilateralFilter(gray, 11, 17, 17)
            edges1 = cv2.Canny(gray_filtered, 30, 150)
            
            # Method 2: Gaussian blur + Canny (different thresholds)
            gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)
            edges2 = cv2.Canny(gray_blur, 20, 100)
            
            # Method 3: Adaptive threshold
            thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                          cv2.THRESH_BINARY, 11, 2)
            edges3 = cv2.Canny(thresh, 30, 100)
            
            # Combine all edge detection methods
            edges = cv2.bitwise_or(edges1, edges2)
            edges = cv2.bitwise_or(edges, edges3)
            
            # Morphological operations
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            edges = cv2.dilate(edges, kernel, iterations=1)
            edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
            
            # Find contours
            contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            self.logger.info(f"Found {len(contours)} contours in vehicle")
            
            # Sort by area and take top 20
            contours = sorted(contours, key=cv2.contourArea, reverse=True)[:20]
            
            candidates = []
            
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                
                # Calculate aspect ratio
                aspect_ratio = w / h if h > 0 else 0
                
                # Calculate relative size (relative to vehicle)
                box_area = w * h
                relative_size = box_area / roi_area if roi_area > 0 else 0
                
                # VERY LENIENT license plate characteristics:
                # - Aspect ratio: 1.3:1 to 8.0:1 (accept almost anything wider than tall)
                # - Size: 0.5% to 40% of vehicle area
                # - Minimum dimensions: 25x10 pixels
                # - Maximum dimensions: 60% of vehicle width/height
                # - Can be anywhere in lower 85% of vehicle
                
                # Log all contours for debugging
                self.logger.debug(f"Contour {contours.index(contour)}: {w}x{h}, aspect={aspect_ratio:.2f}, size={relative_size:.4f}")
                
                if aspect_ratio < 1.3 or aspect_ratio > 8.0:
                    self.logger.debug(f"  → Rejected: aspect_ratio={aspect_ratio:.2f}")
                    continue
                
                if relative_size < 0.005 or relative_size > 0.40:
                    self.logger.debug(f"  → Rejected: relative_size={relative_size:.4f}")
                    continue
                
                if w < 25 or h < 10:
                    self.logger.debug(f"  → Rejected: too small {w}x{h}")
                    continue
                
                if w > roi_width * 0.6 or h > roi_height * 0.6:
                    self.logger.debug(f"  → Rejected: too large {w}x{h}")
                    continue
                
                # Very lenient position check
                if y < roi_height * 0.15:  # Skip only if in top 15% of vehicle
                    self.logger.debug(f"  → Rejected: too high (y={y}/{roi_height})")
                    continue
                
                # Very lenient rectangularity
                rect_area = w * h
                contour_area = cv2.contourArea(contour)
                extent = 0.8
                if contour_area > 0:
                    extent = rect_area / contour_area
                    if extent < 0.4:  # Very lenient - 40%
                        self.logger.debug(f"  → Rejected: extent={extent:.2f}")
                        continue
                
                # Extract plate ROI
                plate_roi = gray[y:y+h, x:x+w]
                if plate_roi.size == 0:
                    continue
                
                # Very lenient edge density check
                plate_edges = cv2.Canny(plate_roi, 20, 150)
                edge_density = np.sum(plate_edges > 0) / plate_roi.size
                
                # Accept almost any edge density (2-50%)
                if edge_density < 0.02 or edge_density > 0.50:
                    self.logger.debug(f"  → Rejected: edge_density={edge_density:.3f}")
                    continue
                
                # Score this candidate
                aspect_score = 2.0 if 1.8 <= aspect_ratio <= 6.0 else 1.0
                score = aspect_ratio * edge_density * extent * aspect_score
                
                self.logger.info(
                    f"✓ CANDIDATE: {w}x{h}, aspect={aspect_ratio:.2f}, "
                    f"edge={edge_density:.3f}, extent={extent:.2f}, score={score:.3f}"
                )
                
                candidates.append((score, x, y, w, h, aspect_ratio, edge_density))
            
            # Sort and take top 5 candidates per vehicle
            candidates.sort(reverse=True, key=lambda x: x[0])
            
            if len(candidates) == 0:
                self.logger.warning(f"⚠️ No candidates found in vehicle region")
            else:
                self.logger.info(f"✅ Found {len(candidates)} candidates, selecting top 5")
            
            for score, x, y, w, h, aspect_ratio, edge_density in candidates[:5]:
                # Create detection with global coordinates
                detection = Detection(
                    id=1,  # Will be reassigned by caller
                    bbox=BoundingBox(
                        x=int(offset_x + x),
                        y=int(offset_y + y),
                        width=int(w),
                        height=int(h)
                    ),
                    confidence=min(0.95, 0.80 + (score / 20)),
                    label="plate"
                )
                detections.append(detection)
                self.logger.info(f"Selected plate candidate with score {score:.3f}")
            
            return detections
            
        except Exception as e:
            self.logger.warning(f"Failed to find plates in region: {e}")
            return []

