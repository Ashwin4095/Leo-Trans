"""FastAPI application entrypoint."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import glossary, health, metrics, submissions, translate
from .core.config import get_settings
from .db.init_db import create_all, seed_glossary
from .db.session import get_sessionmaker


@asynccontextmanager
async def lifespan(app: FastAPI):  # pragma: no cover - framework hook
    await create_all()
    session_factory = get_sessionmaker()
    async with session_factory() as session:
        await seed_glossary(session)
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Leo Translation Orchestrator",
        description=(
            "Manages generation of Thai adaptations with glossary enforcement and "
            "human-in-the-loop workflows."
        ),
        version="0.1.0",
        lifespan=lifespan,
    )

    # CORS configuration – allow frontend origin(s) to call the API
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    app.include_router(health.router)
    app.include_router(glossary.router)
    app.include_router(metrics.router)
    app.include_router(submissions.router)
    app.include_router(translate.router)

    @app.get("/", tags=["root"])
    async def root() -> dict[str, str]:
        return {
            "message": "Leo translation service is running",
            "default_tone": settings.default_tone,
        }

    return app


app = create_app()
