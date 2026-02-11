"""
User model
"""
from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.base import Base


class User(Base):
    """User model - simplified without authentication"""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # User's game/sport performance data (stored as JSON)
    performance_data = Column(JSON, default=dict, nullable=False)
    
    # Relationships
    reports = relationship("Report", back_populates="user", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    progress_records = relationship("Progress", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, name={self.name})>"
