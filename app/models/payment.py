from datetime import date
from decimal import Decimal

from sqlalchemy import Date, String, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


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

    payment_method: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    reference_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    razorpay_order_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    razorpay_payment_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    razorpay_signature: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    rent_obligation = relationship(
        "RentObligation",
        back_populates="payments"
    )