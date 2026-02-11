"""
Progress tracking schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class ProgressCreate(BaseModel):
    """Schema for creating a progress entry"""
    metric_name: str = Field(..., description="Name of the metric being tracked")
    metric_value: float = Field(..., description="Value of the metric")
    metric_unit: Optional[str] = Field(None, description="Unit of measurement")
    activity_type: Optional[str] = Field(None, description="Type of activity")
    notes: Optional[str] = Field(None, description="Additional notes")
    extra_data: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "metric_name": "reaction_time",
                "metric_value": 245.5,
                "metric_unit": "ms",
                "activity_type": "gaming",
                "notes": "After 2 weeks of training",
                "extra_data": {"game": "FPS", "session_duration": 60}
            }
        }


class ProgressResponse(BaseModel):
    """Schema for progress response"""
    id: str
    user_id: str
    metric_name: str
    metric_value: float
    metric_unit: Optional[str]
    activity_type: Optional[str]
    recorded_at: datetime
    notes: Optional[str]
    
    class Config:
        from_attributes = True


class ProgressTrend(BaseModel):
    """Schema for progress trend analysis"""
    metric_name: str
    current_value: float
    starting_value: float
    improvement_percentage: float
    trend: str  # "improving", "declining", "stable"
    data_points: list
