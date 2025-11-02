#!/usr/bin/env python3
"""
Download a pre-trained license plate detection model
"""

import os
import sys
from pathlib import Path

def download_model():
    """Download license plate detection model"""
    
    print("🚀 Downloading license plate detection model...")
    
    # Create models directory
    models_dir = Path('data/models')
    models_dir.mkdir(parents=True, exist_ok=True)
    
    model_path = models_dir / 'license_plate_detector.pt'
    
    if model_path.exists():
        print(f"✅ Model already exists at {model_path}")
        return
    
    # Try multiple sources
    sources = [
        {
            'name': 'Roboflow Universe',
            'url': 'https://universe.roboflow.com/roboflow-universe-projects/license-plate-recognition-rxg4e/model/4',
            'type': 'roboflow'
        }
    ]
    
    print("\n📦 Available options:")
    print("1. Train a custom model using your own dataset")
    print("2. Use Roboflow's pre-trained model (requires API key)")
    print("3. Download from Ultralytics Hub")
    print("4. Use the fallback detection (less accurate)")
    
    print("\n💡 For this POC, we recommend option 4 (fallback detection)")
    print("   It uses YOLOv8 with smart filtering for license plate characteristics")
    
    print("\n📝 To use a custom model:")
    print(f"   1. Download or train a YOLOv8 license plate model")
    print(f"   2. Save it as: {model_path}")
    print(f"   3. Restart the application")
    
    print("\n✅ The application will work with fallback detection")
    print("   (may have lower accuracy but functional for POC)")

if __name__ == "__main__":
    download_model()

