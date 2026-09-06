from uuid import UUID

from database.models.scan import Scan
from database.repositories.scan_repository import ScanRepository


class ScanService:
    """Application logic for scan operations."""

    VALID_SCAN_TYPES = {
        "url",
        "email",
        "sms",
    }

    VALID_PREDICTIONS = {
        "SAFE",
        "PHISHING",
        "SUSPICIOUS",
    }

    VALID_RISKS = {
        "Low",
        "Medium",
        "High",
    }

    def __init__(self, repository: ScanRepository):
        self.repository = repository

    def create_scan(
        self,
        scan_type: str,
        input_content: str,
        prediction: str,
        confidence: float,
        risk: str,
        flag: str | None = None,
        user_id: UUID | None = None,
    ) -> Scan:
        """Validate scan data and persist the scan."""

        scan_type = scan_type.strip().lower()
        prediction = prediction.strip().upper()
        risk = risk.strip().capitalize()

        if scan_type not in self.VALID_SCAN_TYPES:
            raise ValueError(
                f"Invalid scan type: {scan_type}"
            )

        if not input_content.strip():
            raise ValueError(
                "Scan input content cannot be empty."
            )

        if prediction not in self.VALID_PREDICTIONS:
            raise ValueError(
                f"Invalid prediction: {prediction}"
            )

        if not 0 <= confidence <= 1:
            raise ValueError(
                "Confidence must be between 0 and 1."
            )

        if risk not in self.VALID_RISKS:
            raise ValueError(
                f"Invalid risk level: {risk}"
            )

        return self.repository.create(
            user_id=user_id,
            scan_type=scan_type,
            input_content=input_content.strip(),
            prediction=prediction,
            confidence=confidence,
            risk=risk,
            flag=flag,
        )

    def get_scan(
        self,
        scan_id: UUID,
    ) -> Scan | None:
        """Get a scan by UUID."""

        return self.repository.get_by_id(scan_id)

    def get_user_scans(
        self,
        user_id: UUID,
        limit: int = 50,
    ) -> list[Scan]:
        """Get scans belonging to a user."""

        if limit < 1:
            raise ValueError(
                "Limit must be greater than zero."
            )

        limit = min(limit, 100)

        return self.repository.get_by_user(
            user_id=user_id,
            limit=limit,
        )

    def get_recent_scans(
        self,
        limit: int = 50,
    ) -> list[Scan]:
        """Get the most recent scans."""

        if limit < 1:
            raise ValueError(
                "Limit must be greater than zero."
            )

        limit = min(limit, 100)

        return self.repository.get_recent(
            limit=limit,
        )