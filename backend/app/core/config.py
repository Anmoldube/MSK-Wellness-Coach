"""
MSK Wellness AI Chatbot - Configuration
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # App
    APP_NAME: str = "MSK Wellness AI Chatbot"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    
    # Database (using SQLite for development - no PostgreSQL needed!)
    DATABASE_URL: str = "sqlite+aiosqlite:///./msk_chatbot.db"
    
    # AI API Configuration (choose one)
    AI_PROVIDER: str = "anthropic"  # Options: "anthropic", "openai", "gemini", "poe", "groq"
    
    # Anthropic Claude API
    ANTHROPIC_API_KEY: Optional[str] = None
    CLAUDE_MODEL: str = "claude-sonnet-4-20250514"
    
    # OpenAI API
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4"
    
    # Google Gemini API
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-pro"
    
    # Poe API
    POE_API_KEY: Optional[str] = None
    POE_BOT_NAME: str = "GPT-4o-Mini"  # Options: "GPT-4o", "Claude-3.5-Sonnet", "GPT-4o-Mini", etc.
    
    # Groq API (Fast & Free!)
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "llama-3.3-70b-versatile"  # Options: "llama-3.3-70b-versatile", "mixtral-8x7b-32768", "llama-3.1-8b-instant"
    
    # ChromaDB
    CHROMA_PERSIST_DIR: str = "./data/chromadb"
    CHROMA_COLLECTION_NAME: str = "exercise_recommendations"
    
    # File Upload
    UPLOAD_DIR: str = "./data/uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: list = [".pdf", ".jpg", ".jpeg", ".png", ".txt", ".csv"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # CORS - Dynamic for Vercel deployment
    @property
    def ALLOWED_ORIGINS(self) -> list:
        origins = [
            "http://localhost:5173", 
            "http://localhost:3000", 
            "http://frontend:5173",
        ]
        # Add Vercel deployment URLs
        vercel_url = os.getenv("VERCEL_URL")
        if vercel_url:
            origins.append(f"https://{vercel_url}")
        
        # Allow all preview deployments in production
        if not self.DEBUG:
            origins.append("https://*.vercel.app")
        
        return origins
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
