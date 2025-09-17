"""Domain services for translation and localization workflows."""
from dataclasses import dataclass, field
from typing import List, Optional

from ..core.config import Settings
from ..schemas.glossary import GlossaryEntryRead
from .glossary import GlossaryService
from .orchestrator import TranslationOrchestrator, TranslationProviderError
from .prompting import build_translation_prompt


@dataclass
class TranslationResult:
    thai_text: str
    glossary_terms_applied: List[str]
    notes: Optional[str] = None
    prompt: Optional[str] = None
    provider_name: Optional[str] = None
    usage_tokens: Optional[int] = None
    cost_usd: Optional[float] = None
    warnings: List[str] = field(default_factory=list)


class TranslationService:
    """High-level orchestration for generating Thai adaptations."""

    def __init__(
        self,
        settings: Settings,
        glossary_service: GlossaryService | None,
        orchestrator: TranslationOrchestrator | None,
    ) -> None:
        self._settings = settings
        self._glossary_service = glossary_service
        self._orchestrator = orchestrator

    async def translate(
        self,
        english_text: str,
        tone: Optional[str] = None,
        audience: Optional[str] = None,
        channel: Optional[str] = None,
    ) -> TranslationResult:
        """Generate a Thai draft using configured providers with graceful fallback."""

        normalized_tone = tone or self._settings.default_tone
        glossary_entries: List[GlossaryEntryRead] = (
            await self._glossary_service.matched_entries(english_text)
            if self._glossary_service
            else []
        )
        sensitive_entries = [entry for entry in glossary_entries if entry.is_sensitive]
        warnings: List[str] = []
        if sensitive_entries:
            mapped = ", ".join(f"{entry.source_term} → {entry.thai_term}" for entry in sensitive_entries)
            warnings.append(
                "Sensitive glossary terms present: "
                f"{mapped}. Ensure reviewer double-checks cultural nuances."
            )

        prompt = build_translation_prompt(
            english_text=english_text,
            thai_tone=normalized_tone,
            audience=audience,
            channel=channel,
            glossary_entries=glossary_entries,
        )
        provider_output = None
        notes = None

        if self._orchestrator:
            try:
                provider_output = await self._orchestrator.generate(prompt)
            except TranslationProviderError as exc:
                notes = f"Primary providers failed: {exc}. Using placeholder output."

        if provider_output is None:
            draft = self._draft_placeholder(
                english_text=english_text,
                tone=normalized_tone,
                audience=audience,
                channel=channel,
                glossary_entries=glossary_entries,
            )
            provider_name = "placeholder"
            usage_tokens = None
            cost_usd = None
            thai_text = draft
            if notes is None:
                notes = "LLM integration pending or unavailable; placeholder output generated."
        else:
            thai_text = provider_output.thai_text
            provider_name = provider_output.provider_name
            usage_tokens = provider_output.usage_tokens
            cost_usd = provider_output.cost_usd

        for blocked in self._settings.blocked_terms:
            lowered = blocked.lower()
            if lowered in english_text.lower() or lowered in thai_text.lower():
                warnings.append(f"Blocked term detected: '{blocked}'." )

        # De-duplicate warnings while preserving order.
        deduped_warnings: List[str] = []
        for warning in warnings:
            if warning not in deduped_warnings:
                deduped_warnings.append(warning)

        return TranslationResult(
            thai_text=thai_text,
            glossary_terms_applied=[
                f"{entry.source_term} → {entry.thai_term}" for entry in glossary_entries
            ],
            notes=notes,
            prompt=prompt,
            provider_name=provider_name,
            usage_tokens=usage_tokens,
            cost_usd=cost_usd,
            warnings=deduped_warnings,
        )

    def _draft_placeholder(
        self,
        english_text: str,
        tone: str,
        audience: Optional[str],
        channel: Optional[str],
        glossary_entries: List[GlossaryEntryRead],
    ) -> str:
        """Fallback draft generation until LLM orchestration is wired up."""

        components = [
            "[THAI DRAFT PLACEHOLDER]",
            f"Tone: {tone}",
        ]
        if audience:
            components.append(f"Audience: {audience}")
        if channel:
            components.append(f"Channel: {channel}")
        if glossary_entries:
            components.append(
                "Glossary Applied: "
                + ", ".join(f"{entry.source_term} → {entry.thai_term}" for entry in glossary_entries)
            )
        components.append(f"Source: {english_text}")

        return "\n".join(components)
