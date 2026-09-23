from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from enums import TechnicianAvailability


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

    availability_status: Mapped[TechnicianAvailability] = mapped_column(
        String(30),
        default=TechnicianAvailability.AVAILABLE
    )

    contact_reference: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="active"
    )

    assignments = relationship(
        "MaintenanceAssignment",
        back_populates="technician"
    )