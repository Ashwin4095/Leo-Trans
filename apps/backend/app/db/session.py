"""Database session and engine management."""
from collections.abc import AsyncGenerator
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from ..core.config import get_settings

_engine: Optional[AsyncEngine] = None
_sessionmaker: Optional[async_sessionmaker[AsyncSession]] = None
_cached_dsn: Optional[str] = None


def _ensure_engine() -> None:
    global _engine, _sessionmaker, _cached_dsn

    settings = get_settings()
    if _engine is None or _cached_dsn != settings.database_url:
        _engine = create_async_engine(
            settings.database_url,
            echo=settings.database_echo,
            future=True,
        )
        _sessionmaker = async_sessionmaker(bind=_engine, expire_on_commit=False)
        _cached_dsn = settings.database_url


def get_engine() -> AsyncEngine:
    """Return the configured async engine instance."""

    _ensure_engine()
    assert _engine is not None  # for mypy
    return _engine


def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    """Return the configured sessionmaker."""

    _ensure_engine()
    assert _sessionmaker is not None  # for mypy
    return _sessionmaker


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that provides an async database session."""

    session_factory = get_sessionmaker()
    async with session_factory() as session:
        yield session
