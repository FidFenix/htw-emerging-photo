#!/usr/bin/env python3
"""
Download a pre-trained license plate detection model from Roboflow
"""

import os
import sys
from pathlib import Path

def download_model():
    """Download license plate detection model using ultralytics"""
    
    print("🚀 Downloading license plate detection model from Ultralytics Hub...")
    
    try:
        from ultralytics import YOLO
        
        # Create models directory
        models_dir = Path('data/models')
        models_dir.mkdir(parents=True, exist_ok=True)
        
        model_path = models_dir / 'license_plate_detector.pt'
        
        print("\n📦 Attempting to download from Ultralytics Hub...")
        print("   Model: keremberke/yolov8n-license-plate-detection")
        
        # Try to load from Ultralytics Hub - this will download automatically
        try:
            model = YOLO('keremberke/yolov8n-license-plate-detection')
            
            # Save the model locally
            model.save(str(model_path))
            
            print(f"\n✅ Model downloaded successfully!")
            print(f"   Saved to: {model_path}")
            print(f"   Size: {model_path.stat().st_size / 1024:.1f} KB")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Failed to download from Ultralytics Hub: {e}")
            print("\n💡 Alternative options:")
            print("   1. Visit: https://universe.roboflow.com/roboflow-universe-projects/license-plate-recognition-rxg4e")
            print("   2. Download the YOLOv8 model weights")
            print(f"   3. Save as: {model_path}")
            return False
            
    except ImportError:
        print("❌ ultralytics package not found")
        print("   Please install: pip install ultralytics")
        return False

if __name__ == "__main__":
    success = download_model()
    sys.exit(0 if success else 1)

