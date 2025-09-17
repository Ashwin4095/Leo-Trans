"""ORM models for content submissions and review workflow."""
from __future__ import annotations

import uuid
from enum import Enum

from sqlalchemy import JSON, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..db.base import Base, TimestampMixin


class SubmissionStatus(str, Enum):
    EDITING = "editing"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    NEEDS_CHANGES = "needs_changes"


class Submission(TimestampMixin, Base):
    __tablename__ = "submissions"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    source_text: Mapped[str] = mapped_column(Text, nullable=False)
    tone: Mapped[str | None] = mapped_column(String(64), nullable=True)
    audience: Mapped[str | None] = mapped_column(String(128), nullable=True)
    channel: Mapped[str | None] = mapped_column(String(128), nullable=True)

    thai_draft: Mapped[str] = mapped_column(Text, nullable=False)
    thai_final: Mapped[str | None] = mapped_column(Text, nullable=True)
    translation_prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
    provider_name: Mapped[str | None] = mapped_column(String(64), nullable=True)
    usage_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    cost_usd: Mapped[float | None] = mapped_column(Float, nullable=True)

    glossary_terms: Mapped[list[str]] = mapped_column(JSON, default=list)
    warnings: Mapped[list[str]] = mapped_column(JSON, default=list)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    status: Mapped[str] = mapped_column(String(32), default=SubmissionStatus.EDITING.value)
    reviewer_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    last_reviewed_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    def __repr__(self) -> str:  # pragma: no cover - repr helper
        return f"Submission(id={self.id!r}, title={self.title!r}, status={self.status!r})"
