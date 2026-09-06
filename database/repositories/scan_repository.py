from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models.scan import Scan


class ScanRepository:
    """Database operations related to scan records."""

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        scan_type: str,
        input_content: str,
        prediction: str,
        confidence: float,
        risk: str,
        flag: str | None = None,
        user_id: UUID | None = None,
    ) -> Scan:
        """Create and persist a new scan."""

        scan = Scan(
            user_id=user_id,
            scan_type=scan_type,
            input_content=input_content,
            prediction=prediction,
            confidence=confidence,
            risk=risk,
            flag=flag,
        )

        self.db.add(scan)
        self.db.flush()

        return scan

    def get_by_id(
        self,
        scan_id: UUID,
    ) -> Scan | None:
        """Return a scan by UUID."""

        statement = select(Scan).where(
            Scan.id == scan_id
        )

        return self.db.scalar(statement)

    def get_by_user(
        self,
        user_id: UUID,
        limit: int = 50,
    ) -> list[Scan]:
        """Return scans belonging to a specific user."""

        statement = (
            select(Scan)
            .where(Scan.user_id == user_id)
            .order_by(Scan.created_at.desc())
            .limit(limit)
        )

        return list(self.db.scalars(statement).all())

    def get_recent(
        self,
        limit: int = 50,
    ) -> list[Scan]:
        """Return the most recent scans."""

        statement = (
            select(Scan)
            .order_by(Scan.created_at.desc())
            .limit(limit)
        )

        return list(self.db.scalars(statement).all())

    def get_by_scan_type(
        self,
        scan_type: str,
        limit: int = 50,
    ) -> list[Scan]:
        """Return scans filtered by scan type."""

        statement = (
            select(Scan)
            .where(Scan.scan_type == scan_type)
            .order_by(Scan.created_at.desc())
            .limit(limit)
        )

        return list(self.db.scalars(statement).all())

    def count_by_prediction(
        self,
        prediction: str,
    ) -> int:
        """Count scans matching a prediction."""

        statement = select(Scan.id).where(
            Scan.prediction == prediction
        )

        return len(self.db.scalars(statement).all())