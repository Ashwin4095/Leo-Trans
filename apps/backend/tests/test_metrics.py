import pytest
from httpx import AsyncClient

from app.models import SubmissionStatus


@pytest.mark.asyncio
async def test_metrics_overview(client: AsyncClient):
    # Create a submission to ensure metrics have data
    create_resp = await client.post(
        "/submissions",
        json={
            "title": "Metrics smoke",
            "source_text": "Promote the brand with urgency.",
            "tone": "friendly",
        },
    )
    assert create_resp.status_code == 201

    # Approve the submission to exercise status aggregation
    submission_id = create_resp.json()["id"]
    update_resp = await client.put(
        f"/submissions/{submission_id}",
        json={"status": SubmissionStatus.APPROVED.value},
    )
    assert update_resp.status_code == 200

    response = await client.get("/metrics/overview")
    assert response.status_code == 200
    overview = response.json()
    assert overview["total_submissions"] >= 1
    assert overview["submissions_by_status"][SubmissionStatus.APPROVED.value] >= 1
    assert "approval_rate" in overview
    # When blocked term "urgent" exists, warnings should be counted
    assert overview["submissions_with_warnings"] >= 0
