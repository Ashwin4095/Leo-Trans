"""Google Translate API fallback provider."""
from __future__ import annotations

import json
from typing import Any

import httpx

from ...core.config import Settings
from .base import ProviderOutput, TranslationProvider


class GoogleTranslateProvider(TranslationProvider):
    name = "google_translate"

    def __init__(self, settings: Settings) -> None:
        if not settings.google_translate_api_key:
            raise ValueError("Google Translate API key missing")
        self._api_key = settings.google_translate_api_key
        self._endpoint = "https://translation.googleapis.com/language/translate/v2"

    async def generate(self, prompt: str) -> ProviderOutput:
        # For fallback we translate literal text; the prompt format ends with the source content.
        english_text = prompt.split("Content to adapt:\n", 1)[-1].strip()
        payload = {
            "q": english_text,
            "target": "th",
            "format": "text",
        }
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(
                self._endpoint,
                params={"key": self._api_key},
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            data: dict[str, Any] = response.json()

        translations = data.get("data", {}).get("translations", [])
        thai_text = translations[0].get("translatedText", "") if translations else ""
        return ProviderOutput(
            thai_text=thai_text,
            provider_name=self.name,
            raw_prompt=prompt,
            usage_tokens=None,
            cost_usd=None,
        )
