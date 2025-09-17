"""Database initialization helpers."""
from __future__ import annotations

import json
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.config import get_settings
from ..models import GlossaryEntry
from .base import Base
from .session import get_engine


async def create_all() -> None:
    """Create database tables if they do not yet exist."""

    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def seed_glossary(session: AsyncSession) -> None:
    """Load initial glossary entries from the configured seed file."""

    settings = get_settings()
    if not settings.seed_initial_glossary:
        return

    seed_path = Path(settings.initial_glossary_path)
    if not seed_path.exists():
        return

    existing = await session.execute(select(GlossaryEntry.id).limit(1))
    if existing.first():
        return

    with seed_path.open("r", encoding="utf-8") as fh:
        entries = json.load(fh)

    for entry in entries:
        session.add(
            GlossaryEntry(
                source_term=entry["source_term"],
                thai_term=entry["thai_term"],
                part_of_speech=entry.get("part_of_speech"),
                context=entry.get("context"),
                notes=entry.get("notes"),
                is_sensitive=entry.get("is_sensitive", False),
            )
        )

    await session.commit()
