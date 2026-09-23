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
from enums import PaymentMethod, PaymentStatus


class Payment(Base):

    __tablename__ = "payments"

    payment_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    rent_id: Mapped[int] = mapped_column(
        ForeignKey("rent_obligations.rent_id"),
        nullable=False,
        index=True
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    payment_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    payment_method: Mapped[PaymentMethod] = mapped_column(
        String(30),
        nullable=False
    )

    reference_number: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=True
    )

    status: Mapped[PaymentStatus] = mapped_column(
        String(20),
        default=PaymentStatus.SUCCESS
    )

    rent_obligation = relationship(
        "RentObligation",
        back_populates="payments"
    )