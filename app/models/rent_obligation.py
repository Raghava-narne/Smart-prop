from datetime import date
from decimal import Decimal

from sqlalchemy import (
    Date,
    String,
    Numeric,
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class RentObligation(Base):

    __tablename__ = "rent_obligations"

    rent_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    agreement_id: Mapped[int] = mapped_column(
        ForeignKey("rental_agreements.agreement_id"),
        nullable=False,
        index=True
    )

    billing_month: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    due_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    amount_due: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    amount_paid: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    agreement = relationship(
        "RentalAgreement",
        back_populates="rent_obligations"
    )

    payments = relationship(
        "Payment",
        back_populates="rent_obligation"
    )