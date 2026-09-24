from datetime import datetime, timezone

from sqlalchemy import (
    DateTime,
    String,
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


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
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    unassigned_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="assigned"
    )

    ticket = relationship(
        "MaintenanceTicket",
        back_populates="assignments"
    )

    technician = relationship(
        "Technician",
        back_populates="assignments"
    )