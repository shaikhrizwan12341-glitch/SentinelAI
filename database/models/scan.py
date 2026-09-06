import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database.session import Base


class Scan(Base):
    __tablename__ = "scans"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )

    scan_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True
    )

    input_content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    prediction: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    risk: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    flag: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
        index=True
    )