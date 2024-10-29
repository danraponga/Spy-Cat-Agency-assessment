from sqlalchemy import select

from app.db.models.cats import Cat
from app.db.repositories.base import BaseRepository


class CatRepository(BaseRepository):
    async def create(self, data: dict) -> Cat:
        new_cat = Cat(**data)
        self.session.add(new_cat)
        await self.session.flush()
        return new_cat

    async def get_list(self, limit: int) -> list[Cat]:
        stmt = select(Cat).limit(limit)
        return await self.session.scalars(stmt)

    async def get(self, cat_id: int) -> Cat | None:
        stmt = select(Cat).where(Cat.id == cat_id)
        return await self.session.scalar(stmt)
