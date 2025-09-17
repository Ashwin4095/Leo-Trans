"""Pydantic schemas for glossary resources."""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class GlossaryEntryBase(BaseModel):
    source_term: str = Field(..., max_length=255, description="English term to map")
    thai_term: str = Field(..., max_length=255, description="Approved Thai equivalent")
    part_of_speech: Optional[str] = Field(None, max_length=64)
    context: Optional[str] = None
    notes: Optional[str] = None
    is_sensitive: bool = False


class GlossaryEntryCreate(GlossaryEntryBase):
    pass


class GlossaryEntryUpdate(BaseModel):
    thai_term: Optional[str] = Field(None, max_length=255)
    part_of_speech: Optional[str] = Field(None, max_length=64)
    context: Optional[str] = None
    notes: Optional[str] = None
    is_sensitive: Optional[bool] = None


class GlossaryEntryRead(GlossaryEntryBase):
    id: str

    class Config:
        from_attributes = True


class GlossaryEntryList(BaseModel):
    items: list[GlossaryEntryRead]
    total: int
