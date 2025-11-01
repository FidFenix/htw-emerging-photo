"""FastAPI application factory"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import get_settings
from src.utils.logger import setup_logger
from src.api.routes import anonymization


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application
    
    Returns:
        Configured FastAPI app instance
    """
    settings = get_settings()
    
    # Setup logging
    setup_logger("htw-emerging-photo", level=settings.log_level)
    
    # Create app
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Face and License Plate Anonymization API",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # For POC; restrict in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(
        anonymization.router,
        prefix="/api/v1",
        tags=["anonymization"]
    )
    
    # Health check endpoint
    @app.get("/health", tags=["health"])
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "service": settings.app_name,
            "version": settings.app_version
        }
    
    # Startup event to pre-load models
    @app.on_event("startup")
    async def startup_event():
        """Pre-load models on startup to avoid timeout on first request"""
        from src.api.routes.anonymization import get_components
        from src.utils.logger import get_logger
        
        logger = get_logger("startup")
        logger.info("Pre-loading detection models...")
        
        try:
            # This will initialize all detectors
            get_components()
            logger.info("✅ All models loaded successfully")
        except Exception as e:
            logger.error(f"❌ Failed to load models: {e}")
            # Don't fail startup, models will be loaded on first request
    
    return app

