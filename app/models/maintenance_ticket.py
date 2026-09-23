from datetime import datetime

from sqlalchemy import (
    String,
    Text,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from enums import TicketPriority, TicketStatus


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

    priority: Mapped[TicketPriority] = mapped_column(
        String(20),
        default=TicketPriority.MEDIUM
    )

    status: Mapped[TicketStatus] = mapped_column(
        String(30),
        default=TicketStatus.OPEN
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    resolved_at: Mapped[datetime | None] = mapped_column(
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

    assignments = relationship(
        "MaintenanceAssignment",
        back_populates="ticket",
        cascade="all, delete-orphan"
    )