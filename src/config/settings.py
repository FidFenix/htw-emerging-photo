"""Application settings and configuration"""

from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    app_name: str = "HTW Emerging Photo"
    app_version: str = "1.0.0"
    debug: bool = False
    log_level: str = "INFO"
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    max_upload_size: int = 10485760  # 10MB in bytes
    
    # Detection
    face_detection_model: str = "retinaface"
    face_confidence_threshold: float = 0.7
    plate_detection_model: str = "yolo"
    plate_confidence_threshold: float = 0.6
    
    # Anonymization
    anonymization_color: str = "#FFFF00"  # Yellow
    
    # Paths
    models_dir: str = "./data/models"
    uploads_dir: str = "./data/uploads"
    
    # Streamlit
    streamlit_server_port: int = 8501
    streamlit_server_address: str = "0.0.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        protected_namespaces = ('settings_',)  # Avoid model_ namespace conflict


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

