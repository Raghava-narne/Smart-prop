from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db

from app.core.exceptions import AppError

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)

from app.repositories.user_repo import UserRepository

from app.schemas.core import (
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    UserCreate,
    UserResponse,
)

from app.services.auth_services import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)



# LOGIN


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):

    user = AuthService(db).authenticate(
        str(data.email),
        data.password
    )

    token_data = {
        "sub": str(user.user_id),
        "role_id": user.role_id,
    }

    access_token = create_access_token(
        token_data
    )

    refresh_token = create_refresh_token(
        token_data
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }



# REFRESH TOKEN


@router.post(
    "/refresh",
    response_model=TokenResponse
)
def refresh_token(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):

    # Decode refresh token
    payload = decode_refresh_token(
        data.refresh_token
    )

    # Get user ID from token
    user_id = int(payload["sub"])

    # Check user in database
    user = UserRepository(db).get(user_id)

    if not user:
        raise AppError(
            "User not found",
            401
        )

    # Check user status
    if user.status != "active":
        raise AppError(
            "User is inactive",
            403
        )

    # Token data
    token_data = {
        "sub": str(user.user_id),
        "role_id": user.role_id,
    }

    # Create new access token
    new_access_token = create_access_token(
        token_data
    )

    # Create new refresh token
    new_refresh_token = create_refresh_token(
        token_data
    )

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }



# REGISTER

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
def register(
    data: UserCreate,
    db: Session = Depends(get_db),
):

    return AuthService(db).register(data)