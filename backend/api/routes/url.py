from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.schemas.scan import URLScanRequest, ScanResponse
from database.repositories.scan_repository import ScanRepository
from database.services.scan_service import ScanService
from database.session import get_db
from utils.predict_v2 import predict_url


router = APIRouter(
    prefix="/api/v1/scan",
    tags=["URL Scanner"]
)


@router.post(
    "/url",
    response_model=ScanResponse
)
def scan_url(
    request: URLScanRequest,
    db: Session = Depends(get_db),
) -> ScanResponse:

    try:
        # Run ML prediction
        result = predict_url(request.url)

        # Create service
        repository = ScanRepository(db)
        service = ScanService(repository)

        # Save scan to PostgreSQL
        scan = service.create_scan(
            scan_type="url",
            input_content=request.url,
            prediction=result["prediction"],
            confidence=result["confidence"],
            risk=(
                "High"
                if result["prediction"] == "PHISHING"
                else "Low"
            ),
            flag=result.get("flag"),
        )

        # Commit transaction
        db.commit()

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
            detail=str(exc)
        ) from exc

    except FileNotFoundError:
        db.rollback()

        raise HTTPException(
            status_code=503,
            detail="URL scanning model is unavailable."
        )

    except Exception as exc:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="URL scanning failed."
        ) from exc