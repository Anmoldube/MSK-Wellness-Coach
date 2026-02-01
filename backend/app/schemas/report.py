"""
Pydantic Schemas for User and Report data
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, date
from enum import Enum
import uuid


# ============ Enums ============

class ParameterCategory(str, Enum):
    BALANCE = "balance"
    REACTION_TIME = "reaction_time"
    ROM = "rom"
    STRENGTH = "strength"
    FLEXIBILITY = "flexibility"
    ENDURANCE = "endurance"


class RiskLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"


# ============ User Schemas ============

class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    user_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============ Parameter Schemas ============

class UserParameter(BaseModel):
    parameter_name: str = Field(..., description="e.g., 'balance_dynamic'")
    parameter_category: ParameterCategory
    value: float
    unit: str = Field(..., description="e.g., 'seconds', 'degrees', 'score/10'")
    reference_range_min: Optional[float] = None
    reference_range_max: Optional[float] = None
    percentile: Optional[int] = Field(None, ge=0, le=100)
    is_lagging_indicator: bool = True
    is_leading_indicator: bool = False
    interpretation: Optional[str] = None


class ParameterCreate(BaseModel):
    parameter_name: str
    parameter_category: ParameterCategory
    value: float
    unit: str
    reference_range_min: Optional[float] = None
    reference_range_max: Optional[float] = None
    percentile: Optional[int] = None
    is_lagging_indicator: bool = True
    is_leading_indicator: bool = False
    notes: Optional[str] = None


# ============ Report Schemas ============

class AssessmentReportCreate(BaseModel):
    assessment_date: date
    parameters: List[ParameterCreate]
    overall_score: Optional[float] = Field(None, ge=0, le=100)
    risk_level: RiskLevel = RiskLevel.MODERATE


class AssessmentReportResponse(BaseModel):
    report_id: str
    user_id: str
    assessment_date: date
    parameters: List[UserParameter]
    overall_score: Optional[float] = None
    risk_level: RiskLevel
    created_at: datetime
    
    class Config:
        from_attributes = True


class ReportSummary(BaseModel):
    report_id: str
    assessment_date: date
    overall_score: Optional[float]
    risk_level: RiskLevel
    parameter_count: int
