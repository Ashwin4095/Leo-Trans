import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_healthcheck(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_translate_placeholder(client: AsyncClient):
    payload = {
        "text": "Welcome to Leo",
        "tone": "friendly",
    }
    response = await client.post("/translate", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body["thai_text"], str) and len(body["thai_text"]) > 0
    assert isinstance(body["glossary_terms_applied"], list)
    assert body["provider_name"] in {"placeholder", "openai", "google_translate"}
    assert body["prompt"].startswith("You are a senior Thai copywriter")
    assert isinstance(body["warnings"], list)
