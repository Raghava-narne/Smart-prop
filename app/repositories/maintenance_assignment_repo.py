from sqlalchemy.orm import Session

from app.models.maintenance_assignment import MaintenanceAssignment


class MaintenanceAssignmentRepository:

    def __init__(self, db: Session):
        self.db = db

    def add(self, assignment: MaintenanceAssignment):

        self.db.add(assignment)
        self.db.commit()
        self.db.refresh(assignment)

        return assignment

    def get(self, assignment_id: int):

        return (
            self.db
            .query(MaintenanceAssignment)
            .filter(
                MaintenanceAssignment.assignment_id == assignment_id
            )
            .first()
        )

    def get_by_ticket(self, ticket_id: int):

        return (
            self.db
            .query(MaintenanceAssignment)
            .filter(
                MaintenanceAssignment.ticket_id == ticket_id
            )
            .order_by(
                MaintenanceAssignment.assigned_at.desc()
            )
            .first()
        )

    def list(self):

        return (
            self.db
            .query(MaintenanceAssignment)
            .order_by(
                MaintenanceAssignment.assignment_id
            )
            .all()
        )