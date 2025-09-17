"""Glossary CRUD endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query, status

from ...dependencies import get_glossary_service
from ...services.glossary import GlossaryService
from ...schemas.glossary import (
    GlossaryEntryCreate,
    GlossaryEntryList,
    GlossaryEntryRead,
    GlossaryEntryUpdate,
)

router = APIRouter(prefix="/glossary", tags=["glossary"])


@router.get("", response_model=GlossaryEntryList)
async def list_glossary(
    search: str | None = Query(default=None, description="Filter entries by English or Thai term"),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    service: GlossaryService = Depends(get_glossary_service),
) -> GlossaryEntryList:
    return await service.list_entries(search=search, limit=limit, offset=offset)


@router.post("", response_model=GlossaryEntryRead, status_code=status.HTTP_201_CREATED)
async def create_glossary_entry(
    payload: GlossaryEntryCreate,
    service: GlossaryService = Depends(get_glossary_service),
) -> GlossaryEntryRead:
    try:
        return await service.create_entry(payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.get("/{entry_id}", response_model=GlossaryEntryRead)
async def get_glossary_entry(
    entry_id: str,
    service: GlossaryService = Depends(get_glossary_service),
) -> GlossaryEntryRead:
    entry = await service.get_entry(entry_id)
    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return GlossaryEntryRead.model_validate(entry)


@router.put("/{entry_id}", response_model=GlossaryEntryRead)
async def update_glossary_entry(
    entry_id: str,
    payload: GlossaryEntryUpdate,
    service: GlossaryService = Depends(get_glossary_service),
) -> GlossaryEntryRead:
    try:
        return await service.update_entry(entry_id, payload)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_glossary_entry(
    entry_id: str,
    service: GlossaryService = Depends(get_glossary_service),
) -> None:
    try:
        await service.delete_entry(entry_id)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
