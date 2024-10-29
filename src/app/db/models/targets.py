from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base

if TYPE_CHECKING:
    from app.db.models.missions import Mission


class Target(Base):
    __tablename__ = "targets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    mission_id: Mapped[int] = mapped_column(ForeignKey("missions.id"))
    name: Mapped[str] = mapped_column()
    country: Mapped[str] = mapped_column()
    notes: Mapped[str] = mapped_column(nullable=True)
    is_complete: Mapped[bool] = mapped_column(default=False)

    mission: Mapped["Mission"] = relationship("Mission", back_populates="targets")
