from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from database.repositories.user_repository import UserRepository
from database.services.user_service import UserService
from database.session import get_db
from utils.jwt import create_access_token
from utils.security import hash_password, verify_password


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
)
def register_user(
    request: RegisterRequest,
    db: Session = Depends(get_db),
) -> UserResponse:

    try:
        repository = UserRepository(db)
        service = UserService(repository)

        password_hash = hash_password(request.password)

        user = service.create_user(
            email=request.email,
            password_hash=password_hash,
        )

        db.commit()
        db.refresh(user)

        return UserResponse.model_validate(user)

    except ValueError as exc:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="User registration failed.",
        ) from exc


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login_user(
    request: LoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:

    try:
        repository = UserRepository(db)
        service = UserService(repository)

        user = service.get_user_by_email(
            request.email
        )

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password.",
            )

        if not verify_password(
            request.password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password.",
            )

        access_token = create_access_token(
            user.id
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
        )

    except HTTPException:
        raise

    except Exception as exc:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Login failed.",
        ) from exc