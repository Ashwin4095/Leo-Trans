import pytest
from httpx import AsyncClient

from app.schemas.glossary import GlossaryEntryCreate


@pytest.mark.asyncio
async def test_glossary_crud_flow(client: AsyncClient):
    # Initially empty
    response = await client.get("/glossary")
    assert response.status_code == 200
    assert response.json() == {"items": [], "total": 0}

    payload = GlossaryEntryCreate(
        source_term="call to action",
        thai_term="ปุ่มกระตุ้น",
        part_of_speech="phrase",
        context="Marketing CTA copy",
        notes="Focus on persuasive tone",
        is_sensitive=True,
    ).model_dump()

    # Create
    create_resp = await client.post("/glossary", json=payload)
    assert create_resp.status_code == 201
    created = create_resp.json()
    assert created["source_term"] == "call to action"

    entry_id = created["id"]

    # Fetch single
    get_resp = await client.get(f"/glossary/{entry_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["thai_term"] == "ปุ่มกระตุ้น"

    # Update
    update_resp = await client.put(
        f"/glossary/{entry_id}", json={"thai_term": "ปุ่มกระตุ้นการตัดสินใจ"}
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["thai_term"] == "ปุ่มกระตุ้นการตัดสินใจ"

    # Search should match
    search_resp = await client.get("/glossary", params={"search": "ตัดสินใจ"})
    assert search_resp.status_code == 200
    data = search_resp.json()
    assert data["total"] == 1
    assert data["items"][0]["id"] == entry_id

    # Translation should surface glossary mapping
    translate_resp = await client.post(
        "/translate",
        json={
            "text": "This call to action should feel urgent.",
            "tone": "energetic",
        },
    )
    assert translate_resp.status_code == 200
    translation_body = translate_resp.json()
    assert any("call to action" in term for term in translation_body["glossary_terms_applied"])
    assert translation_body["prompt"]
    assert translation_body["provider_name"] in {"placeholder", "openai", "google_translate"}
    assert any("Sensitive glossary terms" in warning for warning in translation_body["warnings"])
    assert any("Blocked term" in warning for warning in translation_body["warnings"])

    # Delete
    delete_resp = await client.delete(f"/glossary/{entry_id}")
    assert delete_resp.status_code == 204

    # Confirm removal
    final_resp = await client.get("/glossary")
    assert final_resp.status_code == 200
    assert final_resp.json() == {"items": [], "total": 0}
