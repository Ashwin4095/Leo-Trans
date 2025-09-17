"""Content submission workflow endpoints."""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from ...dependencies import get_submission_service
from ...models import SubmissionStatus
from ...schemas import SubmissionCreate, SubmissionList, SubmissionRead, SubmissionUpdate
from ...services.exports import ExportService
from ...services.submission import SubmissionService

router = APIRouter(prefix="/submissions", tags=["submissions"])


@router.get("", response_model=SubmissionList)
async def list_submissions(
    status: Optional[SubmissionStatus] = Query(default=None),
    service: SubmissionService = Depends(get_submission_service),
) -> SubmissionList:
    return await service.list_submissions(status=status)


@router.post("", response_model=SubmissionRead, status_code=status.HTTP_201_CREATED)
async def create_submission(
    payload: SubmissionCreate,
    service: SubmissionService = Depends(get_submission_service),
) -> SubmissionRead:
    return await service.create_submission(payload)


@router.get("/{submission_id}", response_model=SubmissionRead)
async def get_submission(
    submission_id: str,
    service: SubmissionService = Depends(get_submission_service),
) -> SubmissionRead:
    submission = await service.get_submission(submission_id)
    if submission is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return SubmissionRead.model_validate(submission)


@router.put("/{submission_id}", response_model=SubmissionRead)
async def update_submission(
    submission_id: str,
    payload: SubmissionUpdate,
    service: SubmissionService = Depends(get_submission_service),
) -> SubmissionRead:
    try:
        return await service.update_submission(submission_id, payload)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/{submission_id}/export")
async def export_submission(
    submission_id: str,
    format: str = Query("csv"),
    service: SubmissionService = Depends(get_submission_service),
) -> Response:
    submission = await service.get_submission(submission_id)
    if submission is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    payload = ExportService(submission).generate(format)
    headers = {"Content-Disposition": f"attachment; filename={payload.filename}"}
    return Response(content=payload.content, media_type=payload.media_type, headers=headers)
