from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user

from app.schemas.core import (
    ApartmentCreate,
    ApartmentUpdate,
    ApartmentResponse,
)

from app.services.apartments_services import ApartmentService
router = APIRouter(tags=["Apartments"])


@router.post(
    "/properties/{property_id}/apartments",
    response_model=ApartmentResponse,
    status_code=201,
)
def create_apartment(
    property_id: int,
    data: ApartmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return ApartmentService(db).create(property_id, data)


@router.get(
    "/properties/{property_id}/apartments",
    response_model=list[ApartmentResponse],
)
def list_property_apartments(
    property_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return ApartmentService(db).list_by_property(property_id)


@router.get(
    "/apartments/{apartment_id}",
    response_model=ApartmentResponse,
)
def get_apartment(
    apartment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return ApartmentService(db).get(apartment_id)


@router.patch(
    "/apartments/{apartment_id}",
    response_model=ApartmentResponse,
)
def update_apartment(
    apartment_id: int,
    data: ApartmentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return ApartmentService(db).update(apartment_id, data)


@router.get(
    "/apartments",
    response_model=list[ApartmentResponse],
)
def filter_apartments(
    status: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = ApartmentService(db)

    if status:
        return service.filter_by_status(status)

    return service.repo.list()