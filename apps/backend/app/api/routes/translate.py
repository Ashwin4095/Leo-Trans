"""Translation orchestration endpoints."""
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from ...dependencies import get_translation_service
from ...services.translation import TranslationResult, TranslationService

router = APIRouter(prefix="/translate", tags=["translation"])


class TranslatePayload(BaseModel):
    text: str = Field(..., description="English source content to translate")
    tone: Optional[str] = Field(None, description="Desired tone for the Thai adaptation")
    audience: Optional[str] = Field(None, description="Target audience to bias localization")
    channel: Optional[str] = Field(None, description="Channel or asset type (ads, social, etc.)")


class TranslateResponse(BaseModel):
    thai_text: str
    glossary_terms_applied: list[str]
    notes: Optional[str] = None
    prompt: Optional[str] = None
    provider_name: Optional[str] = None
    usage_tokens: Optional[int] = None
    cost_usd: Optional[float] = None
    warnings: list[str] = Field(default_factory=list)

    @classmethod
    def from_result(cls, result: TranslationResult) -> "TranslateResponse":
        return cls(
            thai_text=result.thai_text,
            glossary_terms_applied=result.glossary_terms_applied,
            notes=result.notes,
            prompt=result.prompt,
            provider_name=result.provider_name,
            usage_tokens=result.usage_tokens,
            cost_usd=result.cost_usd,
            warnings=result.warnings,
        )


@router.post("", response_model=TranslateResponse)
async def translate(
    payload: TranslatePayload,
    service: TranslationService = Depends(get_translation_service),
) -> TranslateResponse:
    """Produce a Thai draft while honoring glossary and tone requirements."""

    result = await service.translate(
        english_text=payload.text,
        tone=payload.tone,
        audience=payload.audience,
        channel=payload.channel,
    )
    return TranslateResponse.from_result(result)
