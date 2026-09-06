from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.schemas.scan import EmailScanRequest, ScanResponse
from database.repositories.scan_repository import ScanRepository
from database.services.scan_service import ScanService
from database.session import get_db
from utils.predict_email import predict_email


router = APIRouter(
    prefix="/api/v1/scan",
    tags=["Email Scanner"]
)


@router.post(
    "/email",
    response_model=ScanResponse
)
def scan_email(
    request: EmailScanRequest,
    db: Session = Depends(get_db),
) -> ScanResponse:

    try:
        # Run ML prediction
        result = predict_email(request.email_text)

        # Create repository and service
        repository = ScanRepository(db)
        service = ScanService(repository)

        # Save scan to PostgreSQL
        scan = service.create_scan(
            scan_type="email",
            input_content=request.email_text,
            prediction=result["prediction"],
            confidence=result["confidence"],
            risk=result["risk"],
            flag=None,
        )

        # Commit transaction
        db.commit()

        # Return persisted scan
        return ScanResponse(
            scan_type=scan.scan_type,
            prediction=scan.prediction,
            confidence=scan.confidence,
            risk=scan.risk,
            flag=scan.flag,
        )

    except FileNotFoundError:
        db.rollback()

        raise HTTPException(
            status_code=503,
            detail="Email scanning model is unavailable."
        )

    except ValueError as exc:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        ) from exc

    except Exception as exc:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Email scanning failed."
        ) from exc