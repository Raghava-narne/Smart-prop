from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.core import UserCreate, UserUpdate, UserResponse

from app.services.user_services import UserService
router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserResponse, status_code=201)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    return UserService(db).create(data)


@router.get("", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return UserService(db).list()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return UserService(db).get(user_id)
