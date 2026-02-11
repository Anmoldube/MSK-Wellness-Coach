"""
Vercel Serverless Function Entry Point for FastAPI Backend
"""
from app.main import app

# Export the FastAPI app for Vercel
handler = app
