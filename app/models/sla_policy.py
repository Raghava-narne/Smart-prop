from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class SLAPolicy(Base):
    __tablename__ = "sla_policies"

    sla_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    priority: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False
    )

    response_target: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    resolution_target: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )