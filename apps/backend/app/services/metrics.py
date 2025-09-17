"""Analytics and metrics helpers."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Submission, SubmissionStatus
from ..schemas import MetricsOverview


class MetricsService:
    """Aggregate submission and translation metrics."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def overview(self, days: int | None = None) -> MetricsOverview:
        window_clause = None
        if days:
            window_start = datetime.now(timezone.utc) - timedelta(days=days)
            window_clause = Submission.created_at >= window_start

        base_query = select(Submission)
        if window_clause is not None:
            base_query = base_query.where(window_clause)

        submissions = (await self._session.execute(base_query)).scalars().all()

        total_submissions = len(submissions)
        by_status: dict[str, int] = {status.value: 0 for status in SubmissionStatus}
        total_tokens = 0
        total_cost = 0.0
        warnings_count = 0
        approved = 0

        for submission in submissions:
            by_status[submission.status] = by_status.get(submission.status, 0) + 1
            total_tokens += submission.usage_tokens or 0
            total_cost += submission.cost_usd or 0.0
            if submission.warnings:
                warnings_count += 1
            if submission.status == SubmissionStatus.APPROVED.value:
                approved += 1

        average_tokens = (total_tokens / total_submissions) if total_submissions else None
        approval_rate = (approved / total_submissions) if total_submissions else 0.0

        return MetricsOverview(
            total_submissions=total_submissions,
            submissions_by_status=by_status,
            submissions_with_warnings=warnings_count,
            approval_rate=round(approval_rate, 4),
            average_tokens=average_tokens,
            total_tokens=total_tokens,
            total_cost_usd=round(total_cost, 4),
        )
