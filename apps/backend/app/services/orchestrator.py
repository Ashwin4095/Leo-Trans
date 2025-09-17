"""Translation orchestration using primary and fallback providers."""
from __future__ import annotations

from typing import Iterable, Sequence

from tenacity import AsyncRetrying, retry_if_exception_type, stop_after_attempt, wait_exponential

from ..core.config import Settings
from .providers.base import ProviderOutput, TranslationProvider


class TranslationProviderError(RuntimeError):
    """Raised when a provider call fails."""


class TranslationOrchestrator:
    """Coordinate between primary provider and optional fallbacks."""

    def __init__(self, settings: Settings, providers: Sequence[TranslationProvider]) -> None:
        self._settings = settings
        self._providers = providers

    async def generate(self, prompt: str) -> ProviderOutput:
        errors: list[str] = []
        for provider in self._providers:
            try:
                return await self._attempt(provider, prompt)
            except Exception as exc:  # pragma: no cover - defensive fallback
                errors.append(f"{provider.name}: {exc}")
                continue
        raise TranslationProviderError(
            "All translation providers failed: " + "; ".join(errors)
        )

    async def _attempt(self, provider: TranslationProvider, prompt: str) -> ProviderOutput:
        async for attempt in AsyncRetrying(
            retry=retry_if_exception_type(Exception),
            stop=stop_after_attempt(3),
            wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
            reraise=True,
        ):
            with attempt:
                return await provider.generate(prompt)
        raise TranslationProviderError(f"Provider {provider.name} exhausted retries")

    @classmethod
    def from_settings(
        cls,
        settings: Settings,
        provider_factory: Iterable[TranslationProvider],
    ) -> "TranslationOrchestrator":
        providers = list(provider_factory)
        return cls(settings=settings, providers=providers)
