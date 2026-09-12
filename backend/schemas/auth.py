from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    """Request body for user registration."""

    email: EmailStr = Field(
        ...,
        description="User email address",
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="User password",
    )


class LoginRequest(BaseModel):
    """Request body for user login."""

    email: EmailStr = Field(
        ...,
        description="User email address",
    )

    password: str = Field(
        ...,
        min_length=1,
        max_length=128,
        description="User password",
    )


class UserResponse(BaseModel):
    """Public user information."""

    id: UUID
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class TokenResponse(BaseModel):
    """JWT authentication response."""

    access_token: str
    token_type: str = "bearer"