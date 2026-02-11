"""
User schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class PerformanceData(BaseModel):
    """
    Game/Sport performance data schema
    Flexible structure to accommodate different types of metrics
    """
    # Gaming metrics
    reaction_time: Optional[float] = Field(None, description="Average reaction time in milliseconds")
    accuracy: Optional[float] = Field(None, description="Accuracy percentage (0-100)")
    score: Optional[float] = Field(None, description="Game score or rating")
    playtime_hours: Optional[float] = Field(None, description="Hours played per week")
    
    # Physical performance metrics
    endurance: Optional[float] = Field(None, description="Endurance score (0-100)")
    strength: Optional[float] = Field(None, description="Strength score (0-100)")
    flexibility: Optional[float] = Field(None, description="Flexibility score (0-100)")
    balance: Optional[float] = Field(None, description="Balance score (0-100)")
    
    # Additional custom metrics (flexible)
    custom_metrics: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional custom metrics")
    
    class Config:
        json_schema_extra = {
            "example": {
                "reaction_time": 250.5,
                "accuracy": 85.0,
                "score": 2500,
                "playtime_hours": 20,
                "endurance": 70,
                "strength": 65,
                "flexibility": 60,
                "balance": 75,
                "custom_metrics": {
                    "headshot_percentage": 45.2,
                    "win_rate": 62.5
                }
            }
        }


class UserCreate(BaseModel):
    """Schema for creating a new user"""
    name: str = Field(..., min_length=1, max_length=100, description="User's name")
    performance_data: Optional[PerformanceData] = Field(None, description="Initial performance data")


class UserUpdate(BaseModel):
    """Schema for updating user data"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    performance_data: Optional[PerformanceData] = None


class UserResponse(BaseModel):
    """Schema for user response"""
    id: str
    name: str
    performance_data: Dict[str, Any]
    created_at: datetime
    
    class Config:
        from_attributes = True
