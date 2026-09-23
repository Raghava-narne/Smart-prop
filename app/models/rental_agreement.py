from datetime import date
from decimal import Decimal

from sqlalchemy import (
    Date,
    String,
    Numeric,
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from enums import AgreementStatus


class RentalAgreement(Base):

    __tablename__ = "rental_agreements"

    agreement_id: Mapped[int] = mapped_column(
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

    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    end_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    monthly_rent: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    security_deposit: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    status: Mapped[AgreementStatus] = mapped_column(
        String(20),
        default=AgreementStatus.ACTIVE
    )

    tenant = relationship(
        "Tenant",
        back_populates="rental_agreements"
    )

    apartment = relationship(
        "Apartment",
        back_populates="rental_agreements"
    )

    rent_obligations = relationship(
        "RentObligation",
        back_populates="agreement",
        cascade="all, delete-orphan"
    )