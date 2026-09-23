from decimal import Decimal

from sqlalchemy import (
    String,
    Integer,
    Numeric,
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from enums import ApartmentStatus


class Apartment(Base):

    __tablename__ = "apartments"

    apartment_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    property_id: Mapped[int] = mapped_column(
        ForeignKey("properties.property_id"),
        nullable=False,
        index=True
    )

    apartment_number: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    floor_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    apartment_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    monthly_rent: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    status: Mapped[ApartmentStatus] = mapped_column(
        String(30),
        default=ApartmentStatus.AVAILABLE
    )

    property = relationship(
        "Property",
        back_populates="apartments"
    )

    rental_agreements = relationship(
        "RentalAgreement",
        back_populates="apartment"
    )

    maintenance_tickets = relationship(
        "MaintenanceTicket",
        back_populates="apartment"
    )