from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.maintenance import (
    TechnicianCreate,
    TechnicianUpdate,
    TechnicianResponse,
)
from app.services.technician_services import TechnicianService

router = APIRouter(prefix="/technicians", tags=["Technicians"])


@router.post("", response_model=TechnicianResponse, status_code=201)
def create_technician(data: TechnicianCreate, db: Session = Depends(get_db)):
    return TechnicianService(db).create(data)


@router.get("", response_model=list[TechnicianResponse])
def list_technicians(db: Session = Depends(get_db)):
    return TechnicianService(db).list()


@router.get("/{technician_id}", response_model=TechnicianResponse)
def get_technician(technician_id: int, db: Session = Depends(get_db)):
    return TechnicianService(db).get(technician_id)


@router.patch("/{technician_id}/availability", response_model=TechnicianResponse)
def update_availability(
    technician_id: int,
    data: TechnicianUpdate,
    db: Session = Depends(get_db),
):
    return TechnicianService(db).update(technician_id, data)
