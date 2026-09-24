from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base



class Property(Base):

    __tablename__ = "properties"

    property_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    property_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    address_reference: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    owner_reference: Mapped[str] =  mapped _column(
        String(255),
        nullable=False
    )

    number_of_apartments: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    apartments = relationship(
        "Apartment",
        back_populates="property"
    )