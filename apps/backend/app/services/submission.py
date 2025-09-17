"""Submission workflow service."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Submission, SubmissionStatus
from ..schemas import SubmissionCreate, SubmissionList, SubmissionRead, SubmissionUpdate
from .translation import TranslationService


class SubmissionService:
    """Handle submission creation, edits, and review transitions."""

    def __init__(self, session: AsyncSession, translation_service: TranslationService) -> None:
        self._session = session
        self._translation_service = translation_service

    async def create_submission(self, payload: SubmissionCreate) -> SubmissionRead:
        translation = await self._translation_service.translate(
            english_text=payload.source_text,
            tone=payload.tone,
            audience=payload.audience,
            channel=payload.channel,
        )

        submission = Submission(
            title=payload.title.strip(),
            source_text=payload.source_text.strip(),
            tone=payload.tone,
            audience=payload.audience,
            channel=payload.channel,
            thai_draft=translation.thai_text,
            translation_prompt=translation.prompt,
            provider_name=translation.provider_name,
            usage_tokens=translation.usage_tokens,
            cost_usd=translation.cost_usd,
            glossary_terms=translation.glossary_terms_applied,
            warnings=translation.warnings,
            notes=translation.notes,
        )
        self._session.add(submission)
        await self._session.commit()
        await self._session.refresh(submission)
        return SubmissionRead.model_validate(submission)

    async def list_submissions(self, status: SubmissionStatus | None = None) -> SubmissionList:
        statement = select(Submission).order_by(Submission.created_at.desc())
        if status:
            statement = statement.where(Submission.status == status.value)

        result = await self._session.execute(statement)
        items = [SubmissionRead.model_validate(row) for row in result.scalars().all()]

        count_stmt = select(func.count()).select_from(Submission)
        if status:
            count_stmt = count_stmt.where(Submission.status == status.value)
        total = (await self._session.execute(count_stmt)).scalar_one()

        return SubmissionList(items=items, total=total)

    async def get_submission(self, submission_id: str) -> Submission | None:
        result = await self._session.execute(
            select(Submission).where(Submission.id == submission_id)
        )
        return result.scalar_one_or_none()

    async def update_submission(self, submission_id: str, payload: SubmissionUpdate) -> SubmissionRead:
        submission = await self.get_submission(submission_id)
        if submission is None:
            raise LookupError("Submission not found")

        if payload.thai_final is not None:
            submission.thai_final = payload.thai_final.strip()

        if payload.status is not None:
            submission.status = payload.status.value
            submission.last_reviewed_at = datetime.now(timezone.utc)

        if payload.reviewer_notes is not None:
            submission.reviewer_notes = payload.reviewer_notes.strip()

        await self._session.commit()
        await self._session.refresh(submission)
        return SubmissionRead.model_validate(submission)
