"""
MSK Wellness AI Chatbot - Main FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pathlib import Path
import structlog

from app.core.config import settings
from app.api.endpoints import chat, reports, users, recommendations
from app.db.init_db import init_db
from app.utils.logging import configure_logging
from app.services.vector_store import get_vector_store
from app.services.knowledge_base import get_all_exercises

# Configure logging
logger = configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("application_starting", app_name=settings.APP_NAME, version="1.0.0")
    
    # Create data directories
    Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
    Path(settings.CHROMA_PERSIST_DIR).mkdir(parents=True, exist_ok=True)
    
    # Initialize database
    try:
        await init_db()
        logger.info("database_initialized")
    except Exception as e:
        logger.error("database_initialization_failed", error=str(e))
    
    # Initialize vector store and index exercises
    try:
        vector_store = get_vector_store()
        exercises = get_all_exercises()
        if exercises and vector_store.collection.count() == 0:
            vector_store.index_exercises(exercises)
            logger.info("vector_store_initialized", exercises_indexed=len(exercises))
    except Exception as e:
        logger.warning("vector_store_initialization_failed", error=str(e))
        logger.info("continuing_without_vector_store")
    
    logger.info("application_ready", app_name=settings.APP_NAME)
    
    yield
    
    # Shutdown
    logger.info("application_shutting_down", app_name=settings.APP_NAME)


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered chatbot for musculoskeletal wellness analysis and recommendations",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add error handling
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.middleware.error_handler import (
    validation_exception_handler,
    database_exception_handler,
    general_exception_handler,
    ErrorHandlingMiddleware
)
from app.middleware.rate_limiter import limiter, _rate_limit_exceeded_handler, RateLimitExceeded

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, database_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Add rate limiting
try:
    if limiter and RateLimitExceeded and _rate_limit_exceeded_handler:
        app.state.limiter = limiter
        app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
except:
    pass  # Rate limiting optional

# Add request logging middleware
try:
    app.add_middleware(ErrorHandlingMiddleware)
except:
    pass  # Middleware optional

# Include routers
from app.api.endpoints import profile, upload, progress
app.include_router(chat.router, prefix=settings.API_V1_PREFIX, tags=["Chat"])
app.include_router(reports.router, prefix=settings.API_V1_PREFIX, tags=["Reports"])
app.include_router(users.router, prefix=settings.API_V1_PREFIX, tags=["Users"])
app.include_router(recommendations.router, prefix=settings.API_V1_PREFIX, tags=["Recommendations"])
app.include_router(profile.router, prefix=settings.API_V1_PREFIX, tags=["Profile"])
app.include_router(upload.router, prefix=settings.API_V1_PREFIX, tags=["Upload"])
app.include_router(progress.router, prefix=settings.API_V1_PREFIX, tags=["Progress"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to MSK Wellness AI Chatbot API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
