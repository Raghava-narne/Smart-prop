from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.maintenance import (
    SLAPolicyCreate,
    SLAPolicyUpdate,
    SLAPolicyResponse,
     SLAStatusResponse,
)
from app.services.sla_services import SLAService


router = APIRouter(
    prefix="/sla-policies",
    tags=["SLA Policies"]
)


@router.post(
    "",
    response_model=SLAPolicyResponse,
    status_code=201
)
def create_sla(
    data: SLAPolicyCreate,
    db: Session = Depends(get_db)
):
    return SLAService(db).create(data)


@router.get(
    "",
    response_model=list[SLAPolicyResponse]
)
def list_sla(
    db: Session = Depends(get_db)
):
    return SLAService(db).list()


@router.get(
    "/{sla_id}",
    response_model=SLAPolicyResponse
)
def get_sla(
    sla_id: int,
    db: Session = Depends(get_db)
):
    return SLAService(db).get(sla_id)


@router.patch(
    "/{sla_id}",
    response_model=SLAPolicyResponse
)
def update_sla(
    sla_id: int,
    data: SLAPolicyUpdate,
    db: Session = Depends(get_db)
):
    return SLAService(db).update(sla_id, data)


@router.get(
    "/tickets/{ticket_id}",
    response_model=SLAStatusResponse
)

def get_ticket_sla(

    ticket_id: int,

    db: Session = Depends(get_db)

):

    return SLAService(db).get_ticket_sla(
        ticket_id
    )