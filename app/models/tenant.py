from datetime import date

from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base



class Tenant(Base):

    __tablename__ = "tenants"

    tenant_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    full_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    phone_reference: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    identity_reference: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    registration_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    rental_agreements = relationship(
        "RentalAgreement",
        back_populates="tenant"
    )

    maintenance_tickets = relationship(
        "MaintenanceTicket",
        back_populates="tenant"
    )