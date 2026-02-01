"""
Pydantic Schemas for Recommendations
"""
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class RecommendationType(str, Enum):
    CARE_PROGRAM = "care_program"
    EXERCISE = "exercise"
    PRODUCT = "product"


class Difficulty(str, Enum):
    EASY = "easy"
    MODERATE = "moderate"
    HARD = "hard"


class Intensity(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class ProductType(str, Enum):
    SUPPLEMENT = "supplement"
    ERGONOMIC = "ergonomic"
    PAIN_RELIEF = "pain_relief"
    RECOVERY_TOOL = "recovery_tool"


# ============ Care Program Schemas ============

class CareProgram(BaseModel):
    program_id: str
    name: str
    provider: str
    description: str
    focus_areas: List[str]
    duration_weeks: int
    intensity: Intensity
    cost: Optional[float] = None
    match_score: Optional[float] = None
    reasoning: Optional[str] = None


class CareProgramSearchRequest(BaseModel):
    focus_areas: List[str]
    intensity_level: Optional[Intensity] = None
    max_duration_weeks: Optional[int] = None
    limit: int = 5


# ============ Exercise Schemas ============

class Exercise(BaseModel):
    exercise_id: str
    name: str
    category: str
    target_parameters: List[str]
    difficulty: Difficulty
    instructions: List[str]
    sets_reps: str
    frequency: str
    safety_notes: List[str]
    video_url: Optional[str] = None
    expected_timeline: Optional[str] = None


class ExerciseSearchRequest(BaseModel):
    target_parameter: str
    difficulty: Optional[Difficulty] = None
    limit: int = 10


# ============ Product Schemas ============

class Product(BaseModel):
    product_id: str
    name: str
    type: ProductType
    category: str
    description: str
    use_cases: List[str]
    price: Optional[float] = None
    evidence_level: Optional[str] = None
    reasoning: Optional[str] = None


class ProductSearchRequest(BaseModel):
    condition: str
    product_type: Optional[ProductType] = None
    limit: int = 5


# ============ Combined Response ============

class RecommendationResponse(BaseModel):
    recommendation_type: RecommendationType
    items: List[CareProgram | Exercise | Product]
    reasoning: str
    priority_order: Optional[List[str]] = None
