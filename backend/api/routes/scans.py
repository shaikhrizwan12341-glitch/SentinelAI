from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.schemas.scan import (
    ScanHistoryItem,
    ScanHistoryResponse,
)
from database.repositories.scan_repository import ScanRepository
from database.services.scan_service import ScanService
from database.session import get_db


router = APIRouter(
    prefix="/api/v1/scans",
    tags=["Scan History"],
)


@router.get(
    "",
    response_model=ScanHistoryResponse,
)
def get_scan_history(
    limit: int = Query(
        default=50,
        ge=1,
        le=100,
        description="Maximum number of scans to return",
    ),
    db: Session = Depends(get_db),
) -> ScanHistoryResponse:

    try:
        repository = ScanRepository(db)
        service = ScanService(repository)

        scans = service.get_recent_scans(
            limit=limit
        )

        items = [
            ScanHistoryItem.model_validate(scan)
            for scan in scans
        ]

        return ScanHistoryResponse(
            items=items,
            count=len(items),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve scan history.",
        ) from exc


@router.get(
    "/{scan_id}",
    response_model=ScanHistoryItem,
)
def get_scan_by_id(
    scan_id: UUID,
    db: Session = Depends(get_db),
) -> ScanHistoryItem:

    try:
        repository = ScanRepository(db)
        service = ScanService(repository)

        scan = service.get_scan(scan_id)

        if scan is None:
            raise HTTPException(
                status_code=404,
                detail="Scan not found.",
            )

        return ScanHistoryItem.model_validate(scan)

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve scan.",
        ) from exc