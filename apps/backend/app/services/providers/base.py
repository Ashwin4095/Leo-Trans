"""Abstractions for translation providers."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass
class ProviderOutput:
    thai_text: str
    provider_name: str
    raw_prompt: str
    usage_tokens: int | None = None
    cost_usd: float | None = None


class TranslationProvider(Protocol):
    name: str

    async def generate(self, prompt: str) -> ProviderOutput:
        """Produce a Thai adaptation for the supplied prompt."""

        raise NotImplementedError
