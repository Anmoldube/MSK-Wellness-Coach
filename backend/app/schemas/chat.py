"""
Pydantic Schemas for Chat functionality
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatMessage(BaseModel):
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    conversation_id: Optional[str] = None
    include_context: bool = True
    user_id: Optional[str] = None


class FunctionCall(BaseModel):
    name: str
    arguments: Dict[str, Any]
    result: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    message: str
    conversation_id: str
    function_calls: Optional[List[FunctionCall]] = None
    citations: Optional[List[str]] = None
    suggested_questions: Optional[List[str]] = None
    confidence_score: Optional[float] = None


class ConversationSummary(BaseModel):
    conversation_id: str
    started_at: datetime
    message_count: int
    last_message_preview: Optional[str] = None


class ConversationHistory(BaseModel):
    conversation_id: str
    user_id: str
    messages: List[ChatMessage]
    started_at: datetime
    ended_at: Optional[datetime] = None
