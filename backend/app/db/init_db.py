"""
Database initialization utilities
"""
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import Base
from app.db.session import engine
from app.models import User, Report, Conversation, Message, Progress
import structlog

logger = structlog.get_logger()


async def init_db() -> None:
    """
    Initialize database by creating all tables
    """
    try:
        async with engine.begin() as conn:
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error("Error creating database tables", error=str(e))
        raise


async def drop_db() -> None:
    """
    Drop all database tables (use with caution!)
    """
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        logger.info("Database tables dropped successfully")
    except Exception as e:
        logger.error("Error dropping database tables", error=str(e))
        raise


async def reset_db() -> None:
    """
    Reset database by dropping and recreating all tables
    """
    await drop_db()
    await init_db()
