from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user

from app.schemas.maintenance import (
    MaintenanceTicketCreate,
    MaintenanceTicketUpdate,
    MaintenanceTicketResponse,
    AssignTechicianRequest,
    ResolveTicketRequest,
)

from app.services.maintenance_services import MaintenanceService


router = APIRouter(tags=["Maintenance"])


@router.post(
    "/maintenance-tickets",
    response_model=MaintenanceTicketResponse,
    status_code=201
)
def create_ticket(
    data: MaintenanceTicketCreate,
    db: Session = Depends(get_db)
):
    return MaintenanceService(db).create_ticket(data)


@router.get(
    "/maintenance-tickets",
    response_model=list[MaintenanceTicketResponse]
)
def list_tickets(
    status: str | None = Query(default=None),
    db: Session = Depends(get_db)
):
    return MaintenanceService(db).list(status)


@router.get(
    "/maintenance-tickets/{ticket_id}",
    response_model=MaintenanceTicketResponse
)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db)
):
    return MaintenanceService(db).get(ticket_id)


@router.patch(
    "/maintenance-tickets/{ticket_id}/assign",
    response_model=MaintenanceTicketResponse
)
def assign_ticket(
    ticket_id: int,
    data: AssignTechicianRequest,
    db: Session = Depends(get_db)
):
    return MaintenanceService(db).assign(
        ticket_id,
        data.technician_id
    )


@router.patch(
    "/maintenance-tickets/{ticket_id}/start",
    response_model=MaintenanceTicketResponse
)
def start_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return MaintenanceService(db).start(
        ticket_id,
        current_user
    )


@router.patch(
    "/maintenance-tickets/{ticket_id}/resolve",
    response_model=MaintenanceTicketResponse
)
def resolve_ticket(
    ticket_id: int,
    data: ResolveTicketRequest,
    db: Session = Depends(get_db)
):
    return MaintenanceService(db).resolve(
        ticket_id,
        data.resolution_note
    )


@router.patch(
    "/maintenance-tickets/{ticket_id}/close",
    response_model=MaintenanceTicketResponse
)
def close_ticket(
    ticket_id: int,
    db: Session = Depends(get_db)
):
    return MaintenanceService(db).close(ticket_id)


@router.get(
    "/tenants/{tenant_id}/maintenance-tickets",
    response_model=list[MaintenanceTicketResponse]
)
def tenant_tickets(
    tenant_id: int,
    db: Session = Depends(get_db)
):
    return MaintenanceService(db).tenant_tickets(tenant_id)