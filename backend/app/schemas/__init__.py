"""
Pydantic Schemas - Package exports
"""
from app.schemas.report import (
    ParameterCategory,
    RiskLevel,
    UserBase,
    UserCreate,
    UserResponse,
    UserParameter,
    ParameterCreate,
    AssessmentReportCreate,
    AssessmentReportResponse,
    ReportSummary,
)

from app.schemas.chat import (
    MessageRole,
    ChatMessage,
    ChatRequest,
    ChatResponse,
    FunctionCall,
    ConversationSummary,
    ConversationHistory,
)

from app.schemas.recommendation import (
    RecommendationType,
    Difficulty,
    Intensity,
    ProductType,
    CareProgram,
    CareProgramSearchRequest,
    Exercise,
    ExerciseSearchRequest,
    Product,
    ProductSearchRequest,
    RecommendationResponse,
)

__all__ = [
    # Report schemas
    "ParameterCategory",
    "RiskLevel",
    "UserBase",
    "UserCreate",
    "UserResponse",
    "UserParameter",
    "ParameterCreate",
    "AssessmentReportCreate",
    "AssessmentReportResponse",
    "ReportSummary",
    # Chat schemas
    "MessageRole",
    "ChatMessage",
    "ChatRequest",
    "ChatResponse",
    "FunctionCall",
    "ConversationSummary",
    "ConversationHistory",
    # Recommendation schemas
    "RecommendationType",
    "Difficulty",
    "Intensity",
    "ProductType",
    "CareProgram",
    "CareProgramSearchRequest",
    "Exercise",
    "ExerciseSearchRequest",
    "Product",
    "ProductSearchRequest",
    "RecommendationResponse",
]
