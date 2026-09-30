from datetime import datetime, timezone

from app.models.sla_policy import SLAPolicy

from app.repositories.sla_repo import (
    SLAPolicyRepository
)

from app.repositories.maintenance_repo import (
    MaintenanceTicketRepository
)

from app.repositories.maintenance_assignment_repo import (
    MaintenanceAssignmentRepository
)

from app.core.exceptions import AppError


class SLAService:

    def __init__(self, db):

        self.repo = SLAPolicyRepository(db)
        self.ticket_repo = MaintenanceTicketRepository(db)
        self.assignment_repo = MaintenanceAssignmentRepository(db)


    # CREATE

    def create(self, data):

        existing = self.repo.get_by_priority(
            data.priority
        )

        if existing:

            raise AppError(
                "SLA policy for this priority already exists",
                409
            )

        policy = SLAPolicy(
            **data.model_dump()
        )

        return self.repo.add(
            policy
        )


    # LIST

    def list(self):

        return self.repo.list()


    # GET

    def get(self, sla_id):

        policy = self.repo.get(
            sla_id
        )

        if not policy:

            raise AppError(
                "SLA policy not found",
                404
            )

        return policy


    # UPDATE

    def update(
        self,
        sla_id,
        data
    ):

        policy = self.get(
            sla_id
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():

            if value is not None:

                setattr(
                    policy,
                    key,
                    value
                )

        return self.repo.update(
            policy
        )


    # SLA STATUS

    def get_ticket_sla(self, ticket_id):

        ticket = self.ticket_repo.get(
            ticket_id
        )

        if not ticket:

            raise AppError(
                "Maintenance ticket not found",
                404
            )

        policy = self.repo.get_by_priority(
            ticket.priority
        )

        if not policy:

            raise AppError(
                "SLA policy not found for ticket priority",
                404
            )

        assignment = self.assignment_repo.get_by_ticket(
            ticket_id
        )

        if not assignment:

            raise AppError(
                "Maintenance ticket has not been assigned",
                400
            )


        # FIX TIMEZONE DIFFERENCE

        assigned_at = assignment.assigned_at

        created_timestamp = ticket.created_timestamp

        if assigned_at.tzinfo is None:

            assigned_at = assigned_at.replace(
                tzinfo=timezone.utc
            )

        if created_timestamp.tzinfo is None:

            created_timestamp = created_timestamp.replace(
                tzinfo=timezone.utc
            )


        # RESPONSE TIME

        response_time = (
            assigned_at
            - created_timestamp
        )

        response_time_minutes = (
            response_time.total_seconds() / 60
        )

        response_sla_breached = (
            response_time_minutes
            > policy.response_target
        )


        # RESOLUTION TIME

        resolution_time_minutes = None

        resolution_sla_breached = None

        if ticket.resolution_timestamp:

            resolution_timestamp = (
                ticket.resolution_timestamp
            )

            if resolution_timestamp.tzinfo is None:

                resolution_timestamp = (
                    resolution_timestamp.replace(
                        tzinfo=timezone.utc
                    )
                )

            resolution_time = (
                resolution_timestamp
                - assigned_at
            )

            resolution_time_minutes = (
                resolution_time.total_seconds() / 60
            )

            resolution_sla_breached = (
                resolution_time_minutes
                > policy.resolution_target
            )


        return {
            "ticket_id": ticket.ticket_id,

            "priority": ticket.priority,

            "response_time_minutes": round(
                response_time_minutes,
                2
            ),

            "response_target_minutes": (
                policy.response_target
            ),

            "response_sla_breached": (
                response_sla_breached
            ),

            "resolution_time_minutes": (
                round(
                    resolution_time_minutes,
                    2
                )
                if resolution_time_minutes is not None
                else None
            ),

            "resolution_target_minutes": (
                policy.resolution_target
            ),

            "resolution_sla_breached": (
                resolution_sla_breached
            ),

            "status": ticket.status
        }