from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.core import RentalAgreementCreate, RentalAgreementUpdate, RentalResponse
from app.services.rental_services import RentalService
router = APIRouter(tags=["Rental Agreements"])


@router.post("/rental-agreements", response_model=RentalResponse, status_code=201)
def create_agreement(data: RentalAgreementCreate, db: Session = Depends(get_db)):
    return RentalService(db).create(data)


@router.get("/rental-agreements", response_model=list[RentalResponse])
def list_agreements(db: Session = Depends(get_db)):
    return RentalService(db).list()


@router.get("/rental-agreements/{agreement_id}", response_model=RentalResponse)
def get_agreement(agreement_id: int, db: Session = Depends(get_db)):
    return RentalService(db).get(agreement_id)


@router.patch("/rental-agreements/{agreement_id}/terminate", response_model=RentalResponse)
def terminate_agreement(agreement_id: int, db: Session = Depends(get_db)):
    return RentalService(db).terminate(agreement_id)


@router.get("/apartments/{apartment_id}/current-tenant")
def current_tenant(apartment_id: int, db: Session = Depends(get_db)):
    return RentalService(db).current_tenant(apartment_id)
