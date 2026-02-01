"""
Chat API Endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import Optional
import uuid
from datetime import datetime

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ConversationHistory,
    ConversationSummary,
    ChatMessage,
    MessageRole,
)
from app.services.llm_service import LLMService

router = APIRouter(prefix="/chat")

# In-memory storage for demo (replace with database in production)
conversations_db: dict = {}
llm_service = LLMService()


@router.post("/message", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """
    Send a message to the chatbot and get a response
    """
    # Get or create conversation
    if request.conversation_id and request.conversation_id in conversations_db:
        conversation_id = request.conversation_id
        conversation = conversations_db[conversation_id]
    else:
        conversation_id = str(uuid.uuid4())
        conversation = {
            "conversation_id": conversation_id,
            "user_id": "demo-user",
            "messages": [],
            "started_at": datetime.utcnow()
        }
        conversations_db[conversation_id] = conversation
    
    # Add user message
    user_message = ChatMessage(
        role=MessageRole.USER,
        content=request.message,
        timestamp=datetime.utcnow()
    )
    conversation["messages"].append(user_message)
    
    # Get LLM response
    try:
        response = await llm_service.chat(
            user_message=request.message,
            conversation_history=conversation["messages"],
            include_context=request.include_context
        )
        
        # Add assistant message
        assistant_message = ChatMessage(
            role=MessageRole.ASSISTANT,
            content=response["message"],
            timestamp=datetime.utcnow(),
            metadata={
                "function_calls": response.get("function_calls", []),
                "citations": response.get("citations", [])
            }
        )
        conversation["messages"].append(assistant_message)
        
        return ChatResponse(
            message=response["message"],
            conversation_id=conversation_id,
            function_calls=response.get("function_calls"),
            citations=response.get("citations"),
            suggested_questions=response.get("suggested_questions")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")


@router.get("/conversations", response_model=list[ConversationSummary])
async def get_conversations(limit: int = 10, offset: int = 0):
    """
    Get list of user conversations
    """
    conversations = list(conversations_db.values())[offset:offset + limit]
    
    summaries = []
    for conv in conversations:
        messages = conv.get("messages", [])
        last_preview = messages[-1].content[:50] if messages else None
        
        summaries.append(ConversationSummary(
            conversation_id=conv["conversation_id"],
            started_at=conv["started_at"],
            message_count=len(messages),
            last_message_preview=last_preview
        ))
    
    return summaries


@router.get("/conversations/{conversation_id}", response_model=ConversationHistory)
async def get_conversation(conversation_id: str):
    """
    Get a specific conversation with all messages
    """
    if conversation_id not in conversations_db:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    conv = conversations_db[conversation_id]
    
    return ConversationHistory(
        conversation_id=conv["conversation_id"],
        user_id=conv["user_id"],
        messages=conv["messages"],
        started_at=conv["started_at"]
    )


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """
    Delete a conversation
    """
    if conversation_id not in conversations_db:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    del conversations_db[conversation_id]
    return {"status": "deleted"}
