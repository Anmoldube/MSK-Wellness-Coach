"""
Recommendations API Endpoints
"""
from fastapi import APIRouter
from typing import List, Optional

from app.schemas.recommendation import (
    CareProgram,
    Exercise,
    Product,
    Intensity,
    Difficulty,
    ProductType,
)
from app.services.knowledge_base import KnowledgeBaseService

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
    Get exercise recommendations
    """
    exercises = kb_service.search_exercises(
        target_parameter=target_parameter,
        difficulty=difficulty,
        limit=limit
    )
    return exercises


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
