"""Dependency wiring for FastAPI routes."""
from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .core.cache import GlossaryCache
from .core.config import get_settings
from .db.session import get_session
from .services.glossary import GlossaryService
from .services.metrics import MetricsService
from .services.orchestrator import TranslationOrchestrator
from .services.providers.google_translate_provider import GoogleTranslateProvider
from .services.providers.openai_provider import OpenAITranslationProvider
from .services.submission import SubmissionService
from .services.translation import TranslationService

_glossary_cache = GlossaryCache(ttl_seconds=300)
_orchestrator_cache: TranslationOrchestrator | None = None
_orchestrator_providers: tuple[str, ...] | None = None


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Expose an async session for request-scoped usage."""

    async for session in get_session():
        yield session


async def get_glossary_service(
    session: AsyncSession = Depends(get_db_session),
) -> GlossaryService:
    """Provide a GlossaryService wired with the current session."""

    return GlossaryService(session=session, cache=_glossary_cache)


def get_translation_orchestrator() -> TranslationOrchestrator | None:
    """Provide a cached orchestrator based on configured providers."""

    global _orchestrator_cache, _orchestrator_providers

    settings = get_settings()
    providers = []

    try:
        providers.append(OpenAITranslationProvider(settings))
    except ValueError:
        pass

    if settings.fallback_translation_provider == "google_translate":
        try:
            providers.append(GoogleTranslateProvider(settings))
        except ValueError:
            pass

    if not providers:
        _orchestrator_cache = None
        _orchestrator_providers = None
        return None

    provider_names = tuple(provider.name for provider in providers)

    if _orchestrator_cache is None or _orchestrator_providers != provider_names:
        _orchestrator_cache = TranslationOrchestrator(settings=settings, providers=providers)
        _orchestrator_providers = provider_names

    return _orchestrator_cache


def get_translation_service(
    glossary_service: GlossaryService = Depends(get_glossary_service),
    orchestrator: TranslationOrchestrator | None = Depends(get_translation_orchestrator),
) -> TranslationService:
    """Provide a TranslationService instance scoped per request."""

    return TranslationService(
        settings=get_settings(),
        glossary_service=glossary_service,
        orchestrator=orchestrator,
    )


async def get_submission_service(
    session: AsyncSession = Depends(get_db_session),
    translation_service: TranslationService = Depends(get_translation_service),
) -> SubmissionService:
    """Provide the submission workflow service."""

    return SubmissionService(session=session, translation_service=translation_service)


async def get_metrics_service(
    session: AsyncSession = Depends(get_db_session),
) -> MetricsService:
    """Provide analytics helper."""

    return MetricsService(session=session)
