from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class URLScanRequest(BaseModel):
    url: str = Field(
        ...,
        min_length=1,
        max_length=2048,
        description="URL to scan",
    )

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("URL cannot be empty.")

        return value


class EmailScanRequest(BaseModel):
    email_text: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="Email content to scan",
    )

    @field_validator("email_text")
    @classmethod
    def validate_email_text(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Email content cannot be empty.")

        return value


class SMSScanRequest(BaseModel):
    sms_text: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="SMS message to scan",
    )

    @field_validator("sms_text")
    @classmethod
    def validate_sms_text(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("SMS message cannot be empty.")

        return value


class ScanResponse(BaseModel):
    scan_type: str
    prediction: str
    confidence: float
    risk: str
    flag: str | None = None


class ScanHistoryItem(BaseModel):
    id: UUID
    scan_type: str
    input_content: str
    prediction: str
    confidence: float = Field(
        ge=0,
        le=1,
    )
    risk: str
    flag: str | None = None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class ScanHistoryResponse(BaseModel):
    items: list[ScanHistoryItem]
    count: int