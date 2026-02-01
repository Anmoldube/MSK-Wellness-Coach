"""
Users API Endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import List
import uuid
from datetime import datetime

from app.schemas.report import UserCreate, UserResponse

router = APIRouter(prefix="/users")

# In-memory storage for demo
users_db: dict = {
    "demo-user": {
        "user_id": "demo-user",
        "email": "demo@example.com",
        "full_name": "Demo User",
        "created_at": datetime.utcnow()
    }
}


@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate):
    """Create a new user"""
    user_id = str(uuid.uuid4())
    
    new_user = {
        "user_id": user_id,
        "email": user.email,
        "full_name": user.full_name,
        "created_at": datetime.utcnow()
    }
    
    users_db[user_id] = new_user
    return UserResponse(**new_user)


@router.get("/me", response_model=UserResponse)
async def get_current_user():
    """Get current user (demo mode)"""
    return UserResponse(**users_db["demo-user"])


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """Get a specific user"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(**users_db[user_id])
