"""Pydantic schemas for submission workflow."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from ..models import SubmissionStatus


class SubmissionCreate(BaseModel):
    title: str = Field(..., max_length=255)
    source_text: str = Field(..., min_length=1)
    tone: Optional[str] = Field(None, max_length=64)
    audience: Optional[str] = Field(None, max_length=128)
    channel: Optional[str] = Field(None, max_length=128)


class SubmissionUpdate(BaseModel):
    thai_final: Optional[str] = None
    status: Optional[SubmissionStatus] = None
    reviewer_notes: Optional[str] = None


class SubmissionRead(BaseModel):
    id: str
    title: str
    source_text: str
    tone: Optional[str]
    audience: Optional[str]
    channel: Optional[str]
    thai_draft: str
    thai_final: Optional[str]
    translation_prompt: Optional[str]
    provider_name: Optional[str]
    usage_tokens: Optional[int]
    cost_usd: Optional[float]
    glossary_terms: list[str]
    warnings: list[str]
    notes: Optional[str]
    status: SubmissionStatus
    reviewer_notes: Optional[str]
    last_reviewed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SubmissionList(BaseModel):
    items: list[SubmissionRead]
    total: int
