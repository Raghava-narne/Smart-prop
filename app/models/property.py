from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from enums import PropertyStatus


class Property(Base):

    __tablename__ = "properties"

    property_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    owner_id: Mapped[int] = mapped_column(
        nullable=False,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    address: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    number_of_apartments: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    status: Mapped[PropertyStatus] = mapped_column(
        String(20),
        default=PropertyStatus.ACTIVE
    )

    apartments = relationship(
        "Apartment",
        back_populates="property",
        cascade="all, delete-orphan"
    )