"""
Document model for tracking uploaded documents and their indexing status.
"""
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.base import Base


class Document(Base):
    """Tracks uploaded documents and their ChromaDB indexing status"""
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)  # pdf, txt, csv
    page_count = Column(Integer, default=0)
    chunk_count = Column(Integer, default=0)
    status = Column(String, default="processing")  # processing, indexed, failed
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="documents")

    def __repr__(self):
        return f"<Document(id={self.id}, filename={self.filename}, status={self.status})>"
