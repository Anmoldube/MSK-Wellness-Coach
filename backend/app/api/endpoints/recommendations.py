"""
Recommendations API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import structlog

from app.db.session import get_db
from app.models.user import User
from app.schemas.recommendation import (
    CareProgram,
    Exercise,
    Product,
    Intensity,
    Difficulty,
    ProductType,
)
from app.services.knowledge_base import KnowledgeBaseService
from app.services.recommendation_engine import get_recommendation_engine

logger = structlog.get_logger()

router = APIRouter(prefix="/recommendations")

kb_service = KnowledgeBaseService()


@router.get("/care-programs", response_model=List[CareProgram])
async def get_care_programs(
    focus_areas: Optional[str] = None,
    intensity: Optional[Intensity] = None,
    limit: int = 5
):
    """
    Get personalized care program recommendations
    """
    focus_list = focus_areas.split(",") if focus_areas else None
    programs = kb_service.search_care_programs(
        focus_areas=focus_list,
        intensity=intensity,
        limit=limit
    )
    return programs


@router.get("/exercises", response_model=List[Exercise])
async def get_exercises(
    target_parameter: Optional[str] = None,
    difficulty: Optional[Difficulty] = None,
    limit: int = 10
):
    """
    Get exercise recommendations (basic - no user context)
    """
    exercises = kb_service.search_exercises(
        target_parameter=target_parameter,
        difficulty=difficulty,
        limit=limit
    )
    return exercises


@router.get("/exercises/{user_id}")
async def get_personalized_exercises(
    user_id: str,
    limit: int = 5,
    db: AsyncSession = Depends(get_db)
):
    """
    Get personalized exercise recommendations based on user's performance data
    """
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        rec_engine = get_recommendation_engine()
        recommendations = rec_engine.generate_recommendations(
            user_performance_data=user.performance_data,
            limit=limit
        )
        
        logger.info("personalized_exercises_generated", user_id=user_id, count=len(recommendations))
        
        return {
            "user_id": user_id,
            "user_name": user.name,
            "recommendations": recommendations,
            "count": len(recommendations)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("error_generating_personalized_exercises", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate recommendations"
        )


@router.get("/products", response_model=List[Product])
async def get_products(
    condition: Optional[str] = None,
    product_type: Optional[ProductType] = None,
    limit: int = 5
):
    """
    Get product recommendations
    """
    products = kb_service.search_products(
        condition=condition,
        product_type=product_type,
        limit=limit
    )
    return products
