from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class Role(Base):

    __tablename__ = "roles"

    role_id:Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    role_name:Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    users = relationship(
        "User",
        back_populates="role"
    )