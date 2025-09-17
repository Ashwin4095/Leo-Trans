"""Metrics and analytics endpoints."""
from typing import Optional

from fastapi import APIRouter, Depends, Query

from ...dependencies import get_metrics_service
from ...schemas import MetricsOverview
from ...services.metrics import MetricsService

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/overview", response_model=MetricsOverview)
async def get_overview(
    days: Optional[int] = Query(None, ge=1, le=365),
    service: MetricsService = Depends(get_metrics_service),
) -> MetricsOverview:
    """Return aggregate statistics for submissions."""

    return await service.overview(days=days)
