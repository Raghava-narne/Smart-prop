from datetime import datetime, timezone

from app.models.maintenance_ticket import MaintenanceTicket
from app.models.maintenance_assignment import MaintenanceAssignment
from app.models.role import Role

from app.repositories.maintenance_repo import MaintenanceTicketRepository
from app.repositories.tenant_repo import TenantRepository
from app.repositories.apartment_repo import ApartmentRepository
from app.repositories.technician_repo import TechnicianRepository

from app.core.exceptions import AppError
from app.services.audit_services import AuditService


class MaintenanceService:

    def __init__(self, db):
        self.repo = MaintenanceTicketRepository(db)
        self.tenant_repo = TenantRepository(db)
        self.apartment_repo = ApartmentRepository(db)
        self.technician_repo = TechnicianRepository(db)
        self.audit = AuditService(db)

    def create_ticket(self, data):

        tenant = self.tenant_repo.get(data.tenant_id)
        apartment = self.apartment_repo.get(data.apartment_id)

        if not tenant or not apartment:
            raise AppError(
                "Tenant or apartment not found",
                404
            )

        active_agreement = any(
            a.apartment_id == apartment.apartment_id
            and a.status == "ACTIVE"
            for a in tenant.rental_agreements
        )

        if not active_agreement:
            raise AppError(
                "Tenant is not associated with this apartment"
            )

        values = data.model_dump()
        values["status"] = "OPEN"

        ticket = self.repo.add(
            MaintenanceTicket(**values)
        )

        self.audit.log_event(
            event_type="MAINTENANCE_TICKET_CREATED",
            entity_type="MAINTENANCE_TICKET",
            entity_id=ticket.ticket_id,
            actor_reference=None,
            metadata={
                "tenant_id": ticket.tenant_id,
                "apartment_id": ticket.apartment_id,
                "status": ticket.status
            }
        )

        return ticket

    def list(self, status=None):

        if status:
            return self.repo.by_status(status)

        return self.repo.list()

    def get(self, ticket_id):

        obj = self.repo.get(ticket_id)

        if not obj:
            raise AppError(
                "Maintenance ticket not found",
                404
            )

        return obj

    def tenant_tickets(self, tenant_id):

        if not self.tenant_repo.get(tenant_id):
            raise AppError(
                "Tenant not found",
                404
            )

        return self.repo.by_tenant(tenant_id)

    def assign(self, ticket_id, technician_id):

        ticket = self.get(ticket_id)

        technician = self.technician_repo.get(
            technician_id
        )

        if not technician:
            raise AppError(
                "Technician not found",
                404
            )

        if technician.availability_status != "AVAILABLE":
            raise AppError(
                "Technician is not available"
            )

        assignment = MaintenanceAssignment(
            ticket_id=ticket.ticket_id,
            technician_id=technician_id,
            status="ASSIGNED",
        )

        self.repo.db.add(assignment)

        ticket.assigned_technician_id = technician_id
        ticket.status = "ASSIGNED"

        technician.availability_status = "BUSY"

        self.repo.db.commit()

        self.repo.db.refresh(ticket)

        self.audit.log_event(
            event_type="TECHNICIAN_ASSIGNED",
            entity_type="MAINTENANCE_TICKET",
            entity_id=ticket.ticket_id,
            actor_reference=None,
            metadata={
                "technician_id": technician_id,
                "status": ticket.status
            }
        )

        return ticket

    def start(self, ticket_id, current_user):

        ticket = self.get(ticket_id)

        if not ticket.assigned_technician_id:
            raise AppError(
                "Ticket must be assigned before starting"
            )

        if ticket.status != "ASSIGNED":
            raise AppError(
                "Only assigned tickets can be started"
            )

        role_id = current_user.get("role_id")

        if not role_id:
            raise AppError(
                "User role not found",
                403
            )

        role = (
            self.repo.db.query(Role)
            .filter(Role.role_id == int(role_id))
            .first()
        )

        if not role:
            raise AppError(
                "User role not found",
                403
            )

        if role.role_name.upper() != "TECHNICIAN":
            raise AppError(
                "Only technicians can start maintenance work",
                403
            )

        ticket.status = "IN_PROGRESS"

        self.repo.db.commit()

        self.repo.db.refresh(ticket)

        self.audit.log_event(
            event_type="MAINTENANCE_STARTED",
            entity_type="MAINTENANCE_TICKET",
            entity_id=ticket.ticket_id,
            actor_reference=current_user.get("sub"),
            metadata={
                "technician_id": ticket.assigned_technician_id,
                "status": ticket.status
            }
        )

        return ticket

    def resolve(self, ticket_id, resolution_note):

        ticket = self.get(ticket_id)

        if not ticket.assigned_technician_id:
            raise AppError(
                "Ticket must have an assigned technician"
            )

        if ticket.status != "IN_PROGRESS":
            raise AppError(
                "Only tickets in progress can be resolved"
            )

        ticket.status = "RESOLVED"

        ticket.resolution_timestamp = datetime.now(
            timezone.utc
        )

        ticket.resolution_note = resolution_note

        self.repo.db.commit()

        self.repo.db.refresh(ticket)

        self.audit.log_event(
            event_type="MAINTENANCE_RESOLVED",
            entity_type="MAINTENANCE_TICKET",
            entity_id=ticket.ticket_id,
            actor_reference=None,
            metadata={
                "technician_id": ticket.assigned_technician_id,
                "status": ticket.status,
                "resolution_note": resolution_note
            }
        )

        return ticket

    def close(self, ticket_id):

        ticket = self.get(ticket_id)

        if ticket.status != "RESOLVED":
            raise AppError(
                "Only resolved tickets can be closed"
            )

        ticket.status = "CLOSED"

        if ticket.assigned_technician_id:

            technician = self.technician_repo.get(
                ticket.assigned_technician_id
            )

            if technician:
                technician.availability_status = "AVAILABLE"

        self.repo.db.commit()

        self.repo.db.refresh(ticket)

        self.audit.log_event(
            event_type="MAINTENANCE_CLOSED",
            entity_type="MAINTENANCE_TICKET",
            entity_id=ticket.ticket_id,
            actor_reference=None,
            metadata={
                "technician_id": ticket.assigned_technician_id,
                "status": ticket.status
            }
        )

        return ticket