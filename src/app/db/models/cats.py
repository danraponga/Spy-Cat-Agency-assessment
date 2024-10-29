from typing import TYPE_CHECKING

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base

if TYPE_CHECKING:
    from app.db.models.missions import Mission


class Cat(Base):
    __tablename__ = "cats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    years_of_experience: Mapped[int] = mapped_column()
    breed: Mapped[str] = mapped_column()
    salary: Mapped[int] = mapped_column()

    mission: Mapped["Mission"] = relationship(
        "Mission", back_populates="cat", uselist=False
    )
