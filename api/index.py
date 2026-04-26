"""
Vercel Serverless Entry Point
Wraps the FastAPI app for Vercel serverless functions with proper DB initialization.
"""
import sys
import os
from pathlib import Path
from contextlib import asynccontextmanager

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import structlog

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup: create DB tables if they don't exist.
    This is safe to run on every cold start — create_all is idempotent.
    """
    try:
        from app.db.init_db import init_db
        await init_db()
        logger.info("serverless_db_initialized")
    except Exception as e:
        # Log but don't crash — app can still serve static files / health checks
        logger.error("serverless_db_init_failed", error=str(e))

    # Skip ChromaDB indexing in serverless — no persistent /tmp between invocations.
    # Knowledge base falls back to keyword search automatically.

    yield
    # No explicit teardown needed for serverless


# Create app with lifespan
from app.core.config import settings

app = FastAPI(
    title="MSK Wellness AI Chatbot",
    description="AI-powered chatbot for musculoskeletal wellness analysis and recommendations",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
from app.api.endpoints import chat, reports, users, recommendations, profile, upload, progress
app.include_router(chat.router, prefix=settings.API_V1_PREFIX, tags=["Chat"])
app.include_router(reports.router, prefix=settings.API_V1_PREFIX, tags=["Reports"])
app.include_router(users.router, prefix=settings.API_V1_PREFIX, tags=["Users"])
app.include_router(recommendations.router, prefix=settings.API_V1_PREFIX, tags=["Recommendations"])
app.include_router(profile.router, prefix=settings.API_V1_PREFIX, tags=["Profile"])
app.include_router(upload.router, prefix=settings.API_V1_PREFIX, tags=["Upload"])
app.include_router(progress.router, prefix=settings.API_V1_PREFIX, tags=["Progress"])


@app.get("/api")
async def root():
    """API Root endpoint"""
    return {
        "message": "Welcome to MSK Wellness AI Chatbot API",
        "docs": "/api/docs",
        "version": "1.0.0"
    }


@app.get("/api/health")
async def health_check():
    """Health check — also reports DB connectivity"""
    import sqlalchemy
    db_status = "unknown"
    try:
        from app.db.session import engine
        async with engine.connect() as conn:
            await conn.execute(sqlalchemy.text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "status": "healthy",
        "environment": "serverless",
        "database": db_status,
    }


# Serve frontend static assets
frontend_dir = Path(__file__).parent.parent / "frontend" / "dist"

if (frontend_dir / "assets").exists():
    app.mount("/assets", StaticFiles(directory=str(frontend_dir / "assets")), name="assets")


@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    """Serve frontend static files or index.html for SPA routing"""
    if full_path.startswith("api"):
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Not Found")

    file_path = frontend_dir / full_path
    if file_path.is_file():
        return FileResponse(file_path)

    index_file = frontend_dir / "index.html"
    if index_file.exists():
        return FileResponse(index_file)

    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Frontend not found")
