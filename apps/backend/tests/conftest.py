import os

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.core.config import get_settings
from app.main import create_app


@pytest_asyncio.fixture
async def client(tmp_path):
    os.environ["LEO_DATABASE_URL"] = f"sqlite+aiosqlite:///{tmp_path}/test.db"
    os.environ["LEO_SEED_INITIAL_GLOSSARY"] = "false"
    os.environ["LEO_BLOCKED_TERMS"] = "[\"urgent\"]"
    get_settings.cache_clear()  # type: ignore[attr-defined]
    app = create_app()
    transport = ASGITransport(app=app)
    async with app.router.lifespan_context(app):
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            yield client
