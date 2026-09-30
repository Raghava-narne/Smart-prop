from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import create_access_token
from app.schemas.core import LoginRequest, TokenResponse, UserCreate, UserResponse
from app.services.auth_services import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


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

    access_token = create_access_token(
        {
            "sub": str(user.user_id),
            "role_id": user.role_id,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


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