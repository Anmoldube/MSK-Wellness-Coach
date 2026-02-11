"""
User Profile and Performance Data Management Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Dict, Any
import structlog

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse, PerformanceData

logger = structlog.get_logger()

router = APIRouter()


@router.post("/profile", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user_profile(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new user profile with game/sport performance data
    
    No authentication required - users just provide their name and performance metrics
    """
    try:
        # Create new user
        new_user = User(
            name=user_data.name,
            performance_data=user_data.performance_data.dict() if user_data.performance_data else {}
        )
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        logger.info("user_profile_created", user_id=new_user.id, name=new_user.name)
        
        return UserResponse(
            id=new_user.id,
            name=new_user.name,
            performance_data=new_user.performance_data,
            created_at=new_user.created_at
        )
        
    except Exception as e:
        logger.error("error_creating_user_profile", error=str(e))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user profile"
        )


@router.get("/profile/{user_id}", response_model=UserResponse)
async def get_user_profile(
    user_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get user profile by ID"""
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserResponse(
            id=user.id,
            name=user.name,
            performance_data=user.performance_data,
            created_at=user.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("error_fetching_user_profile", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch user profile"
        )


@router.put("/profile/{user_id}", response_model=UserResponse)
async def update_user_profile(
    user_id: str,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update user profile and performance data"""
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Update fields
        if user_data.name:
            user.name = user_data.name
        if user_data.performance_data:
            user.performance_data = user_data.performance_data.dict()
        
        await db.commit()
        await db.refresh(user)
        
        logger.info("user_profile_updated", user_id=user_id)
        
        return UserResponse(
            id=user.id,
            name=user.name,
            performance_data=user.performance_data,
            created_at=user.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("error_updating_user_profile", user_id=user_id, error=str(e))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user profile"
        )


@router.get("/profile/{user_id}/performance-summary")
async def get_performance_summary(
    user_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a summary of user's performance metrics
    """
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        perf_data = user.performance_data
        
        # Generate summary
        summary = {
            "user_id": user_id,
            "name": user.name,
            "total_metrics": len(perf_data),
            "metrics": perf_data,
            "strengths": _identify_strengths(perf_data),
            "areas_for_improvement": _identify_weaknesses(perf_data)
        }
        
        return summary
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("error_generating_performance_summary", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate performance summary"
        )


def _identify_strengths(perf_data: Dict[str, Any]) -> list:
    """Identify user's strengths based on performance data"""
    strengths = []
    
    # Example logic - can be customized based on your metrics
    for metric, value in perf_data.items():
        if isinstance(value, (int, float)):
            if value >= 80:  # High score threshold
                strengths.append(metric)
    
    return strengths


def _identify_weaknesses(perf_data: Dict[str, Any]) -> list:
    """Identify areas for improvement based on performance data"""
    weaknesses = []
    
    # Example logic - can be customized based on your metrics
    for metric, value in perf_data.items():
        if isinstance(value, (int, float)):
            if value < 50:  # Low score threshold
                weaknesses.append(metric)
    
    return weaknesses
