from datetime import datetime,timezone

from sqlalchemy import (
    String,
    Text,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base



class MaintenanceTicket(Base):

    __tablename__ = "maintenance_tickets"

    ticket_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenants.tenant_id"),
        nullable=False,
        index=True
    )

    apartment_id: Mapped[int] = mapped_column(
        ForeignKey("apartments.apartment_id"),
        nullable=False,
        index=True
    )

    complaint_category: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    priority: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="open"
    )

    created_timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    assigned_technician_id: Mapped[int | None] = mapped_column(
        ForeignKey("technicians.technician_id"),
        nullable=True,
    )

    resolution_timestamp: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    tenant = relationship(
        "Tenant",
        back_populates="maintenance_tickets"
    )

    apartment = relationship(
        "Apartment",
        back_populates="maintenance_tickets"
    )

    technician = relationship(
        "Technician",
        foreign_keys = [assigned_technician] 
    )

    assignments = relationship(
        "MaintenanceAssignment",
        back_populates="ticket"
    )