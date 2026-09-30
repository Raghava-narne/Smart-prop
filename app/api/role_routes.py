from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.core import RoleCreate, RoleUpdate, RoleResponse
from app.services.role_services import RoleService

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.post("", response_model=RoleResponse, status_code=201)

def create_role(data: RoleCreate, db: Session = Depends(get_db)):

    return RoleService(db).create(data)


@router.get("", response_model=list[RoleResponse])

def list_roles(db: Session = Depends(get_db)):

    return RoleService(db).list()


@router.get("/{role_id}", response_model=RoleResponse)

def get_role(role_id: int, db: Session = Depends(get_db)):

    return RoleService(db).get(role_id)


@router.patch("/{role_id}", response_model=RoleResponse)

def update_role(role_id: int, data: RoleUpdate, db: Session = Depends(get_db)):

    return RoleService(db).update(role_id, data)