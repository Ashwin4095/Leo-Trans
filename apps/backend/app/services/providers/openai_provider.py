"""OpenAI-backed translation provider."""
from __future__ import annotations

from typing import Optional

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion

from ...core.config import Settings
from .base import ProviderOutput, TranslationProvider


class OpenAITranslationProvider(TranslationProvider):
    name = "openai"

    def __init__(self, settings: Settings) -> None:
        if not settings.openai_api_key:
            raise ValueError("OpenAI API key missing")
        self._client = AsyncOpenAI(api_key=settings.openai_api_key)
        self._model = settings.openai_model
        self._temperature = settings.openai_temperature

    async def generate(self, prompt: str) -> ProviderOutput:
        completion: ChatCompletion = await self._client.chat.completions.create(  # type: ignore[assignment]
            model=self._model,
            temperature=self._temperature,
            messages=[
                {"role": "system", "content": "You are a Thai localization expert."},
                {"role": "user", "content": prompt},
            ],
        )

        message = completion.choices[0].message.content or ""
        usage = completion.usage
        usage_tokens: Optional[int] = usage.total_tokens if usage else None
        cost_usd: Optional[float] = None

        return ProviderOutput(
            thai_text=message.strip(),
            provider_name=self.name,
            raw_prompt=prompt,
            usage_tokens=usage_tokens,
            cost_usd=cost_usd,
        )
