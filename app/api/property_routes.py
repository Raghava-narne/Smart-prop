from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user

from app.schemas.core import (
    PropertyCreate,
    PropertyUpdate,
    PropertyResponse,
)

from app.services.property_services import PropertyService


router = APIRouter(
    prefix="/properties",
    tags=["Properties"]
)


@router.post(
    "",
    response_model=PropertyResponse,
    status_code=201
)
def create_property(
    data: PropertyCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return PropertyService(db).create(data)


@router.get(
    "",
    response_model=list[PropertyResponse]
)
def list_properties(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return PropertyService(db).list()


@router.get(
    "/{property_id}",
    response_model=PropertyResponse
)
def get_property(
    property_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return PropertyService(db).get(property_id)


@router.patch(
    "/{property_id}",
    response_model=PropertyResponse
)
def update_property(
    property_id: int,
    data: PropertyUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return PropertyService(db).update(
        property_id,
        data
    )


@router.delete(
    "/{property_id}"
)
def delete_property(
    property_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return PropertyService(db).delete(property_id)