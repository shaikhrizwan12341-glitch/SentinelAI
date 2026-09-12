from uuid import UUID

from database.models.scan import Scan
from database.repositories.scan_repository import ScanRepository


class ScanService:
    """Business logic for scan records."""

    VALID_SCAN_TYPES = {"url", "email", "sms"}
    VALID_PREDICTIONS = {"SAFE", "PHISHING", "SUSPICIOUS"}
    VALID_RISKS = {"Low", "Medium", "High"}

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
        """Validate and create a scan record."""

        scan_type = scan_type.strip().lower()
        prediction = prediction.strip().upper()
        risk = risk.strip()

        if scan_type not in self.VALID_SCAN_TYPES:
            raise ValueError(
                f"Invalid scan type: {scan_type}"
            )

        if prediction not in self.VALID_PREDICTIONS:
            raise ValueError(
                f"Invalid prediction: {prediction}"
            )

        if risk not in self.VALID_RISKS:
            raise ValueError(
                f"Invalid risk: {risk}"
            )

        if not input_content or not input_content.strip():
            raise ValueError(
                "Input content cannot be empty."
            )

        if not 0 <= confidence <= 1:
            raise ValueError(
                "Confidence must be between 0 and 1."
            )

        return self.repository.create(
            user_id=user_id,
            scan_type=scan_type,
            input_content=input_content.strip(),
            prediction=prediction,
            confidence=float(confidence),
            risk=risk,
            flag=flag,
        )

    def get_scan(
        self,
        scan_id: UUID,
        user_id: UUID | None = None,
    ) -> Scan | None:
        """Return a scan, optionally restricted to its owner."""

        return self.repository.get_by_id(
            scan_id=scan_id,
            user_id=user_id,
        )

    def get_user_scans(
        self,
        user_id: UUID,
        limit: int = 50,
    ) -> list[Scan]:
        """Return scans belonging to a specific user."""

        if limit < 1:
            raise ValueError(
                "Limit must be at least 1."
            )

        limit = min(limit, 100)

        return self.repository.get_by_user(
            user_id=user_id,
            limit=limit,
        )

    def get_recent_scans(
        self,
        limit: int = 50,
        user_id: UUID | None = None,
    ) -> list[Scan]:
        """Return recent scans, optionally restricted to a user."""

        if limit < 1:
            raise ValueError(
                "Limit must be at least 1."
            )

        limit = min(limit, 100)

        return self.repository.get_recent(
            limit=limit,
            user_id=user_id,
        )

    def get_filtered_scans(
        self,
        limit: int = 50,
        offset: int = 0,
        scan_type: str | None = None,
        prediction: str | None = None,
        user_id: UUID | None = None,
    ) -> list[Scan]:
        """Return filtered scans belonging to a specific user."""

        if limit < 1:
            raise ValueError(
                "Limit must be at least 1."
            )

        if limit > 100:
            limit = 100

        if offset < 0:
            raise ValueError(
                "Offset cannot be negative."
            )

        if scan_type is not None:
            scan_type = scan_type.strip().lower()

            if scan_type not in self.VALID_SCAN_TYPES:
                raise ValueError(
                    f"Invalid scan type: {scan_type}"
                )

        if prediction is not None:
            prediction = prediction.strip().upper()

            if prediction not in self.VALID_PREDICTIONS:
                raise ValueError(
                    f"Invalid prediction: {prediction}"
                )

        return self.repository.get_filtered(
            limit=limit,
            offset=offset,
            scan_type=scan_type,
            prediction=prediction,
            user_id=user_id,
        )