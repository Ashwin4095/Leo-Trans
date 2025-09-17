import pytest
from httpx import AsyncClient

from app.models import SubmissionStatus


@pytest.mark.asyncio
async def test_submission_flow(client: AsyncClient):
    # Create submission
    payload = {
        "title": "March campaign CTA",
        "source_text": "Promote the new brand launch with a limited time offer.",
        "tone": "energetic",
        "audience": "Millennial shoppers",
        "channel": "social",
    }
    create_resp = await client.post("/submissions", json=payload)
    assert create_resp.status_code == 201
    submission = create_resp.json()
    assert submission["status"] == SubmissionStatus.EDITING.value
    assert isinstance(submission["thai_draft"], str) and submission["thai_draft"]
    assert submission["translation_prompt"].startswith("You are a senior Thai copywriter")

    submission_id = submission["id"]

    # List submissions shows one entry
    list_resp = await client.get("/submissions")
    assert list_resp.status_code == 200
    summary = list_resp.json()
    assert summary["total"] == 1
    assert summary["items"][0]["id"] == submission_id

    # Update final text and submit for review
    update_resp = await client.put(
        f"/submissions/{submission_id}",
        json={
            "thai_final": "ใส่สำเนาไทยฉบับตรวจแล้ว",
            "status": SubmissionStatus.IN_REVIEW.value,
        },
    )
    assert update_resp.status_code == 200
    updated = update_resp.json()
    assert updated["thai_final"] == "ใส่สำเนาไทยฉบับตรวจแล้ว"
    assert updated["status"] == SubmissionStatus.IN_REVIEW.value

    # Reviewer marks approved with notes
    review_resp = await client.put(
        f"/submissions/{submission_id}",
        json={
            "status": SubmissionStatus.APPROVED.value,
            "reviewer_notes": "Looks good",
        },
    )
    assert review_resp.status_code == 200
    approved = review_resp.json()
    assert approved["status"] == SubmissionStatus.APPROVED.value
    assert approved["reviewer_notes"] == "Looks good"
    assert approved["last_reviewed_at"] is not None

    # Filter by status
    list_approved = await client.get("/submissions", params={"status": SubmissionStatus.APPROVED.value})
    assert list_approved.status_code == 200
    approved_summary = list_approved.json()
    assert approved_summary["total"] == 1

    # Export CSV
    export_csv = await client.get(f"/submissions/{submission_id}/export", params={"format": "csv"})
    assert export_csv.status_code == 200
    assert export_csv.headers["content-type"].startswith("text/csv")

    # Export DOCX
    export_docx = await client.get(f"/submissions/{submission_id}/export", params={"format": "docx"})
    assert export_docx.status_code == 200
    assert export_docx.headers["content-type"].startswith(
        "application/vnd.openxmlformats-officedocument"
    )

    # Export social TXT
    export_social = await client.get(
        f"/submissions/{submission_id}/export", params={"format": "social"}
    )
    assert export_social.status_code == 200
    assert export_social.headers["content-type"].startswith("text/plain")
