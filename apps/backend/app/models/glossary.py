"""ORM model for glossary entries."""
from __future__ import annotations

import uuid

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..db.base import Base, TimestampMixin


class GlossaryEntry(TimestampMixin, Base):
    __tablename__ = "glossary_entries"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False
    )
    source_term: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    thai_term: Mapped[str] = mapped_column(String(255), nullable=False)
    part_of_speech: Mapped[str | None] = mapped_column(String(64), nullable=True)
    context: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_sensitive: Mapped[bool] = mapped_column(default=False, nullable=False)

    def __repr__(self) -> str:  # pragma: no cover - repr helper
        return f"GlossaryEntry(id={self.id!r}, source_term={self.source_term!r})"
