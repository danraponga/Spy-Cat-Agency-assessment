from typing import AsyncIterable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.cat_repository import CatRepository
from app.db.repositories.mission_respository import MissionRepository
from app.db.setup import SessionLocal


async def get_session() -> AsyncIterable[AsyncSession]:
    async with SessionLocal() as session:
        yield session


async def get_cat_repository(session=Depends(get_session)):
    return CatRepository(session)


async def get_mission_repository(session=Depends(get_session)):
    return MissionRepository(session)
