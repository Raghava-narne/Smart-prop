from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base



class Technician(Base):

    __tablename__ = "technicians"

    technician_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    specialization: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    availability_status: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    contact_reference: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

    assignments = relationship(
        "MaintenanceAssignment",
        back_populates="technician"
    )

    assigned_tickets = relationship(
        "MaintenanceTicket",
        foreign_keys="MaintenanceTicket.assigned_technician",
        back_populates="technician"
    )