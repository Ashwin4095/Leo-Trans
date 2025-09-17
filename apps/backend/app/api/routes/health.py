"""Healthcheck routes."""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["health"])
async def healthcheck() -> dict[str, str]:
    """Return a simple service health indicator."""

    return {"status": "ok"}
