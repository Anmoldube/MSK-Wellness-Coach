"""
Report model for storing user performance reports
"""
from sqlalchemy import Column, String, DateTime, JSON, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.base import Base


class Report(Base):
    """Report model for game/sport performance assessments"""
    __tablename__ = "reports"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Report metadata
    title = Column(String, nullable=False)
    report_type = Column(String, nullable=False)  # e.g., "game_performance", "sport_assessment"
    
    # Performance metrics (stored as JSON)
    metrics = Column(JSON, default=dict, nullable=False)
    
    # File attachment (if uploaded)
    file_path = Column(String, nullable=True)
    file_name = Column(String, nullable=True)
    
    # Analysis results
    analysis_summary = Column(Text, nullable=True)
    risk_score = Column(Float, nullable=True)  # 0-100 scale
    
    # Relationships
    user = relationship("User", back_populates="reports")
    
    def __repr__(self):
        return f"<Report(id={self.id}, user_id={self.user_id}, title={self.title})>"
