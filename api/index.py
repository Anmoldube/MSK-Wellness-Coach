"""
Vercel Serverless Entry Point
This file wraps the FastAPI app for Vercel's serverless functions
"""
import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

# Import FastAPI without triggering lifespan events
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create a minimal app without complex initialization for serverless
app = FastAPI(
    title="MSK Wellness AI Chatbot",
    description="AI-powered chatbot for musculoskeletal wellness analysis and recommendations",
    version="1.0.0",
)

# Configure CORS
from app.core.config import settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
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
    """Health check endpoint"""
    return {"status": "healthy", "environment": "serverless"}

# Mount static files from frontend dist
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import os

# Get the frontend dist directory
frontend_dir = Path(__file__).parent.parent / "frontend" / "dist"

# Mount assets directory for JS, CSS, and other static files
if (frontend_dir / "assets").exists():
    app.mount("/assets", StaticFiles(directory=str(frontend_dir / "assets")), name="assets")

@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    """Serve frontend static files or index.html for SPA routing"""
    # If it's an API route, let FastAPI handle it normally
    if full_path.startswith("api"):
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Not Found")
    
    # Check if it's a static file request
    file_path = frontend_dir / full_path
    if file_path.is_file():
        return FileResponse(file_path)
    
    # Otherwise serve index.html for SPA routing
    index_file = frontend_dir / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    else:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Frontend not found")
