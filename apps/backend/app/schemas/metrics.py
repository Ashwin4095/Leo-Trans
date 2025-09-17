"""Pydantic schemas describing analytics responses."""
from __future__ import annotations

from datetime import datetime
from typing import Dict

from pydantic import BaseModel, Field


class MetricsOverview(BaseModel):
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    total_submissions: int
    submissions_by_status: Dict[str, int]
    submissions_with_warnings: int
    approval_rate: float
    average_tokens: float | None
    total_tokens: int
    total_cost_usd: float

