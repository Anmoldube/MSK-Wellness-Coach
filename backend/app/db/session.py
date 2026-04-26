"""
Database session management
Supports PostgreSQL (Neon/hosted) and SQLite (local dev).
"""
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

_db_url = settings.DATABASE_URL
if _db_url.startswith("postgres://"):
    _db_url = _db_url.replace("postgres://", "postgresql+asyncpg://", 1)
elif _db_url.startswith("postgresql://") and not _db_url.startswith("postgresql+asyncpg://"):
    _db_url = _db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

_is_postgres = _db_url.startswith("postgresql")
_is_local = any(h in _db_url for h in ["localhost", "127.0.0.1"])

if _is_postgres:
    # Serverless-safe pool for Neon / hosted PostgreSQL
    # Small pool prevents connection exhaustion in serverless environments
    _connect_args = {} if _is_local else {"ssl": "require"}  # Local Postgres doesn't need SSL
    _engine_kwargs = dict(
        pool_pre_ping=True,
        pool_size=2,
        max_overflow=5,
        pool_recycle=300,        # recycle connections every 5 min
        pool_timeout=30,
        connect_args=_connect_args,
    )
else:
    # SQLite (local development) — no pool_size for NullPool-compatible usage
    _engine_kwargs = dict(
        pool_pre_ping=True,
        connect_args={"check_same_thread": False},
    )

from sqlalchemy import event

# Create async engine
engine = create_async_engine(
    _db_url,
    echo=settings.DEBUG,
    future=True,
    **_engine_kwargs,
)

@event.listens_for(engine.sync_engine, "do_connect")
def receive_do_connect(dialect, conn_rec, cargs, cparams):
    # asyncpg < 0.30.0 sometimes gets `channel_binding` from SQLAlchemy 
    # but doesn't support it, causing connection crashes.
    # It also doesn't support `sslmode` or `options` which are commonly in Neon URLs.
    for kwarg in ["channel_binding", "sslmode", "options"]:
        if kwarg in cparams:
            del cparams[kwarg]

# Create async session maker
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncSession:
    """
    Dependency for getting async database sessions.
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
