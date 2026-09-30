from sqlalchemy.orm import Session

from app.models.maintenance_ticket import MaintenanceTicket


class MaintenanceTicketRepository:

    def __init__(self, db: Session):
        self.db = db

    def add(self, ticket: MaintenanceTicket):
        self.db.add(ticket)
        self.db.commit()
        self.db.refresh(ticket)
        return ticket

    def list(self):
        return self.db.query(MaintenanceTicket).all()

    def get(self, ticket_id: int):
        return (
            self.db.query(MaintenanceTicket)
            .filter(MaintenanceTicket.ticket_id == ticket_id)
            .first()
        )

    def by_tenant(self, tenant_id: int):
        return (
            self.db.query(MaintenanceTicket)
            .filter(MaintenanceTicket.tenant_id == tenant_id)
            .all()
        )

    def by_apartment(self, apartment_id: int):
        return (
            self.db.query(MaintenanceTicket)
            .filter(MaintenanceTicket.apartment_id == apartment_id)
            .all()
        )

    def by_status(self, status: str):
        return (
            self.db.query(MaintenanceTicket)
            .filter(MaintenanceTicket.status == status)
            .all()
        )