from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.core import RentObligationCreate, RentObligationUpdate, RentObligationResponse
from app.services.rent_services import RentService

router = APIRouter(tags=["Rent"])


@router.post("/rent-obligations/generate", response_model=RentObligationResponse, status_code=201)
def generate_rent(data: RentObligationCreate, db: Session = Depends(get_db)):
    return RentService(db).generate(data)


@router.get("/rent-obligations", response_model=list[RentObligationResponse])
def list_rent(db: Session = Depends(get_db)):
    return RentService(db).list()


@router.get("/tenants/{tenant_id}/rent", response_model=list[RentObligationResponse])
def tenant_rent(tenant_id: int, db: Session = Depends(get_db)):
    return RentService(db).tenant_rent(tenant_id)

@router.patch(
    "/rent-obligations/{rent_id}",
    response_model=RentObligationResponse
)
def update_rent(
    rent_id: int,
    data: RentObligationUpdate,
    db: Session = Depends(get_db)
):

    return RentService(db).update(rent_id, data)
