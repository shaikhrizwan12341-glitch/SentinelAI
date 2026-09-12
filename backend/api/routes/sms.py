import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.api.dependencies import get_current_user
from backend.schemas.scan import SMSScanRequest, ScanResponse
from database.models.user import User
from database.repositories.scan_repository import ScanRepository
from database.services.scan_service import ScanService
from database.session import get_db
from utils.predict_sms import predict_sms


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/api/v1/sms",
    tags=["SMS Scanner"],
)


@router.post(
    "/scan",
    response_model=ScanResponse,
)
def scan_sms(
    request: SMSScanRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ScanResponse:

    try:
        result = predict_sms(request.sms_text)

        repository = ScanRepository(db)
        service = ScanService(repository)

        scan = service.create_scan(
            user_id=current_user.id,
            scan_type="sms",
            input_content=request.sms_text,
            prediction=result["prediction"],
            confidence=float(result["confidence"]),
            risk=result["risk"],
            flag=result.get("flag"),
        )

        db.commit()
        db.refresh(scan)

        return ScanResponse(
            scan_type=scan.scan_type,
            prediction=scan.prediction,
            confidence=scan.confidence,
            risk=scan.risk,
            flag=scan.flag,
        )

    except ValueError as exc:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except HTTPException:
        db.rollback()
        raise

    except Exception as exc:
        db.rollback()

        logger.exception(
            "SMS scan failed: %s",
            exc,
        )

        raise HTTPException(
            status_code=500,
            detail="SMS scan failed.",
        ) from exc