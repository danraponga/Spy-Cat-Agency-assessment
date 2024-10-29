from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.base import Base


class BaseRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _commit(self) -> None:
        await self.session.commit()

    async def _delete(self, obj: Base):
        await self.session.delete(obj)
