from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base

if TYPE_CHECKING:
    from app.db.models.cats import Cat
    from app.db.models.targets import Target


class Mission(Base):
    __tablename__ = "missions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cat_id: Mapped[int] = mapped_column(ForeignKey("cats.id"), nullable=True)
    is_complete: Mapped[bool] = mapped_column(default=False)

    cat: Mapped["Cat"] = relationship("Cat", back_populates="mission")
    targets: Mapped[list["Target"]] = relationship(
        "Target",
        back_populates="mission",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
