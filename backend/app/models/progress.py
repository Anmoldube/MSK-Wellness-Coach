"""
Progress tracking model
"""
from sqlalchemy import Column, String, DateTime, JSON, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.base import Base


class Progress(Base):
    """Progress model for tracking user improvement over time"""
    __tablename__ = "progress"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Progress metrics
    metric_name = Column(String, nullable=False)  # e.g., "reaction_time", "accuracy", "endurance"
    metric_value = Column(Float, nullable=False)
    metric_unit = Column(String, nullable=True)  # e.g., "ms", "%", "score"
    
    # Contextual data
    activity_type = Column(String, nullable=True)  # e.g., "gaming", "training", "assessment"
    notes = Column(Text, nullable=True)
    extra_data = Column(JSON, default=dict, nullable=False)  # Renamed from 'metadata' (reserved word)
    
    # Relationships
    user = relationship("User", back_populates="progress_records")
    
    def __repr__(self):
        return f"<Progress(id={self.id}, user_id={self.user_id}, metric={self.metric_name}={self.metric_value})>"
