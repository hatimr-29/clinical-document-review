import os
from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    APP_NAME: str = "ClinReview AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # API & CORS
    API_PREFIX: str = "/api"
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://localhost:8000",
        "*"
    ]
    
    # Database
    DATABASE_URL: str = "sqlite:///./clinreview.db"
    
    # AI/ML Provider Configuration
    AI_PROVIDER: str = "mock"  # "openai", "gemini", "custom", or "mock"
    AI_API_KEY: Optional[str] = None
    AI_MODEL: str = "gpt-4o-mini"
    AI_BASE_URL: Optional[str] = None
    
    # Document Limits
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_IMAGE_TYPES: List[str] = ["image/png", "image/jpeg", "image/jpg"]
    ALLOWED_PDF_TYPES: List[str] = ["application/pdf"]
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
