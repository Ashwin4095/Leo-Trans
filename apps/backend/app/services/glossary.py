"""Service layer for glossary CRUD operations."""
from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.cache import GlossaryCache
from ..models import GlossaryEntry
from ..schemas.glossary import (
    GlossaryEntryCreate,
    GlossaryEntryList,
    GlossaryEntryRead,
    GlossaryEntryUpdate,
)


class GlossaryService:
    """Encapsulate glossary persistence and querying logic."""

    def __init__(self, session: AsyncSession, cache: GlossaryCache | None = None) -> None:
        self._session = session
        self._cache = cache

    async def list_entries(
        self,
        search: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> GlossaryEntryList:
        entries = await self._load_all_entries()

        if search:
            lowered = search.lower()
            entries = [
                entry
                for entry in entries
                if lowered in entry.source_term.lower() or lowered in entry.thai_term.lower()
            ]

        total = len(entries)
        window = entries[offset : offset + limit]
        return GlossaryEntryList(items=window, total=total)

    async def get_entry(self, entry_id: str) -> GlossaryEntry | None:
        result = await self._session.execute(
            select(GlossaryEntry).where(GlossaryEntry.id == entry_id)
        )
        return result.scalar_one_or_none()

    async def create_entry(self, payload: GlossaryEntryCreate) -> GlossaryEntryRead:
        entry = GlossaryEntry(**payload.model_dump())
        self._session.add(entry)
        try:
            await self._session.commit()
        except IntegrityError as exc:  # pragma: no cover - defensive guard
            await self._session.rollback()
            raise ValueError("Duplicate source term") from exc
        await self._session.refresh(entry)
        await self._invalidate_cache()
        return GlossaryEntryRead.model_validate(entry)

    async def update_entry(self, entry_id: str, payload: GlossaryEntryUpdate) -> GlossaryEntryRead:
        entry = await self.get_entry(entry_id)
        if entry is None:
            raise LookupError("Glossary entry not found")

        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(entry, field, value)

        try:
            await self._session.commit()
        except IntegrityError as exc:  # pragma: no cover - defensive guard
            await self._session.rollback()
            raise ValueError("Duplicate source term") from exc
        await self._session.refresh(entry)
        await self._invalidate_cache()
        return GlossaryEntryRead.model_validate(entry)

    async def delete_entry(self, entry_id: str) -> None:
        entry = await self.get_entry(entry_id)
        if entry is None:
            raise LookupError("Glossary entry not found")
        await self._session.delete(entry)
        await self._session.commit()
        await self._invalidate_cache()

    async def matched_entries(self, english_text: str) -> list[GlossaryEntryRead]:
        entries = await self._load_all_entries()
        lower_text = english_text.lower()
        matched: list[GlossaryEntryRead] = []
        for entry in entries:
            if entry.source_term.lower() in lower_text:
                matched.append(entry)
        return matched

    async def _load_all_entries(self) -> list[GlossaryEntryRead]:
        if self._cache:
            cached = await self._cache.get_entries()
            if cached is not None:
                return [GlossaryEntryRead.model_validate(item) for item in cached]

        result = await self._session.execute(
            select(GlossaryEntry).order_by(GlossaryEntry.source_term)
        )
        entries = [GlossaryEntryRead.model_validate(entry) for entry in result.scalars().all()]

        if self._cache:
            await self._cache.set_entries([entry.model_dump() for entry in entries])

        return entries

    async def _invalidate_cache(self) -> None:
        if self._cache:
            await self._cache.invalidate()
