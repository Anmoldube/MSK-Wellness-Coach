"""
Chat API Endpoints
Uses PostgreSQL via SQLAlchemy to persist conversations and messages.
Integrates document RAG for context-aware responses.
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ConversationHistory,
    ConversationSummary,
    ChatMessage,
    MessageRole,
)
from app.models.user import User
from app.models.conversation import Conversation, Message
from app.services.llm_service import LLMService
from app.services.document_service import get_document_service
from app.db.session import get_db

router = APIRouter(prefix="/chat")
llm_service = LLMService()


@router.post("/message", response_model=ChatResponse)
@router.post("/send", response_model=ChatResponse)
async def send_message(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    """
    Send a message to the chatbot and get a response.
    Persists messages to PostgreSQL.
    Retrieves relevant document chunks (RAG) for context.
    """
    # Fetch user context from DB
    user_context = None
    if request.user_id:
        try:
            result = await db.execute(select(User).where(User.id == request.user_id))
            user = result.scalar_one_or_none()
            if user:
                user_context = {
                    "user_id": user.id,
                    "name": user.name,
                    "performance_data": user.performance_data or {}
                }
        except Exception as e:
            print(f"Error fetching user profile: {e}")

    # Get or create conversation in DB
    conversation_id = request.conversation_id
    is_new_conversation = False
    if conversation_id:
        result = await db.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        conversation = result.scalar_one_or_none()
        if not conversation:
            conversation_id = None

    if not conversation_id:
        is_new_conversation = True
        conversation = Conversation(
            id=str(uuid.uuid4()),
            user_id=request.user_id or "demo-user",
            title=request.message[:50].strip(),  # Auto-title from first message
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(conversation)
        await db.flush()  # Get the ID without committing yet
        conversation_id = conversation.id

    # Get current message count for sequence
    count_result = await db.execute(
        select(func.count(Message.id)).where(Message.conversation_id == conversation_id)
    )
    message_count = count_result.scalar() or 0

    # Save user message to DB
    user_msg_db = Message(
        id=str(uuid.uuid4()),
        conversation_id=conversation_id,
        role="user",
        content=request.message,
        sequence=message_count + 1,
        created_at=datetime.utcnow(),
    )
    db.add(user_msg_db)
    await db.flush()

    # Build history from DB for LLM context (last 10 messages)
    history_result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.sequence.desc())
        .limit(10)
    )
    history_db = history_result.scalars().all()
    conversation_history = [
        ChatMessage(role=MessageRole(m.role), content=m.content, timestamp=m.created_at)
        for m in reversed(history_db)
    ]

    # --- RAG: Search user's uploaded documents for relevant context ---
    rag_sources = []
    rag_context = ""
    if request.user_id:
        try:
            doc_service = get_document_service()
            chunks = doc_service.search_user_documents(
                query=request.message,
                user_id=request.user_id,
                n_results=3,
            )
            if chunks:
                rag_parts = ["[Relevant context from your uploaded documents:]"]
                for chunk in chunks:
                    meta = chunk.get("metadata", {})
                    rag_parts.append(
                        f"--- From '{meta.get('filename', 'document')}' (page {meta.get('page', '?')}) ---\n"
                        f"{chunk['text'][:500]}"
                    )
                    rag_sources.append({
                        "filename": meta.get("filename", ""),
                        "page": meta.get("page", 1),
                        "doc_id": meta.get("doc_id", ""),
                    })
                rag_context = "\n\n".join(rag_parts)
        except Exception as e:
            print(f"RAG search error (non-fatal): {e}")

    # Get LLM response
    try:
        response = await llm_service.chat(
            user_message=request.message,
            conversation_history=conversation_history,
            include_context=request.include_context,
            user_context=user_context,
            rag_context=rag_context,
        )

        message_content = response.get("response") or response.get("message", "")

        # Save assistant message to DB
        assistant_msg_db = Message(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            role="assistant",
            content=message_content,
            sequence=message_count + 2,
            created_at=datetime.utcnow(),
        )
        db.add(assistant_msg_db)

        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()

        await db.commit()

        return ChatResponse(
            message=message_content,
            conversation_id=conversation_id,
            function_calls=response.get("function_calls"),
            citations=response.get("citations"),
            suggested_questions=response.get("suggestions") or response.get("suggested_questions", []),
            rag_sources=rag_sources if rag_sources else None,
        )

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")


@router.get("/conversations", response_model=list[ConversationSummary])
async def get_conversations(
    user_id: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """Get list of conversations from PostgreSQL"""
    query = select(Conversation).order_by(Conversation.updated_at.desc()).offset(offset).limit(limit)
    if user_id:
        query = query.where(Conversation.user_id == user_id)

    result = await db.execute(query)
    conversations = result.scalars().all()

    summaries = []
    for conv in conversations:
        # Get last message preview
        last_msg_result = await db.execute(
            select(Message)
            .where(Message.conversation_id == conv.id)
            .order_by(Message.sequence.desc())
            .limit(1)
        )
        last_msg = last_msg_result.scalar_one_or_none()

        msg_count_result = await db.execute(
            select(func.count(Message.id)).where(Message.conversation_id == conv.id)
        )
        msg_count = msg_count_result.scalar() or 0

        summaries.append(ConversationSummary(
            conversation_id=conv.id,
            title=conv.title,
            started_at=conv.created_at,
            message_count=msg_count,
            last_message_preview=last_msg.content[:50] if last_msg else None
        ))

    return summaries


@router.get("/conversations/{conversation_id}", response_model=ConversationHistory)
async def get_conversation(conversation_id: str, db: AsyncSession = Depends(get_db)):
    """Get a specific conversation with all messages from PostgreSQL"""
    result = await db.execute(
        select(Conversation).where(Conversation.id == conversation_id)
    )
    conv = result.scalar_one_or_none()

    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    msgs_result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.sequence)
    )
    messages_db = msgs_result.scalars().all()

    messages = [
        ChatMessage(role=MessageRole(m.role), content=m.content, timestamp=m.created_at)
        for m in messages_db
    ]

    return ConversationHistory(
        conversation_id=conv.id,
        user_id=conv.user_id,
        messages=messages,
        started_at=conv.created_at,
    )


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str, db: AsyncSession = Depends(get_db)):
    """Delete a conversation and its messages from PostgreSQL"""
    result = await db.execute(
        select(Conversation).where(Conversation.id == conversation_id)
    )
    conv = result.scalar_one_or_none()

    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    await db.delete(conv)
    await db.commit()
    return {"status": "deleted"}
