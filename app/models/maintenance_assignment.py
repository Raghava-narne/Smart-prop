from datetime import datetime

from sqlalchemy import (
    DateTime,
    String,
    Text,
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from enums import AssignmentStatus


class MaintenanceAssignment(Base):

    __tablename__ = "maintenance_assignments"

    assignment_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    ticket_id: Mapped[int] = mapped_column(
        ForeignKey("maintenance_tickets.ticket_id"),
        nullable=False,
        index=True
    )

    technician_id: Mapped[int] = mapped_column(
        ForeignKey("technicians.technician_id"),
        nullable=False,
        index=True
    )

    assigned_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    unassigned_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    status: Mapped[AssignmentStatus] = mapped_column(
        String(30),
        default=AssignmentStatus.ASSIGNED
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    ticket = relationship(
        "MaintenanceTicket",
        back_populates="assignments"
    )

    technician = relationship(
        "Technician",
        back_populates="assignments"
    )