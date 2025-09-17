"""Prompt template helpers for translation orchestration."""
from __future__ import annotations

from typing import Iterable, Optional

from ..schemas.glossary import GlossaryEntryRead

PROMPT_HEADER = (
    "You are a senior Thai copywriter. Translate and adapt English marketing content into Thai\n"
    "so that it feels natively written. Preserve meaning while matching the requested tone,"
    " audience, and channel."
)


def _format_glossary(entries: Iterable[GlossaryEntryRead]) -> str:
    items = [f"- {entry.source_term} → {entry.thai_term}" for entry in entries]
    return "\n".join(items) if items else "- (no enforced terms)"


def build_translation_prompt(
    english_text: str,
    thai_tone: str,
    audience: Optional[str],
    channel: Optional[str],
    glossary_entries: Iterable[GlossaryEntryRead],
) -> str:
    """Construct the base prompt supplied to the LLM orchestrator."""

    sections = [PROMPT_HEADER]
    sections.append(f"Desired tone: {thai_tone}")
    if audience:
        sections.append(f"Target audience: {audience}")
    if channel:
        sections.append(f"Channel: {channel}")
    sections.append("Glossary requirements:\n" + _format_glossary(glossary_entries))
    sections.append("Content to adapt:\n" + english_text.strip())
    sections.append(
        "Output must be polished Thai copy. Avoid literal word-for-word translation and respect "
        "cultural nuances. Highlight any ambiguous phrases in a reviewer note section."
    )
    return "\n\n".join(sections)
