from sqlalchemy import select

from app.db.models.missions import Mission
from app.db.models.targets import Target
from app.db.repositories.base import BaseRepository


class MissionRepository(BaseRepository):
    async def create(self, data: dict) -> Mission:
        mission = Mission(**data)
        self.session.add(mission)
        await self.session.flush()
        return mission

    async def create_target(self, data: dict) -> Target:
        target = Target(**data)
        self.session.add(target)
        await self.session.flush()
        return target

    async def get_list(self, limit: int) -> list[Mission]:
        stmt = select(Mission).limit(limit)
        return await self.session.scalars(stmt)

    async def get(self, mission_id: int) -> Mission | None:
        stmt = select(Mission).where(Mission.id == mission_id)
        return await self.session.scalar(stmt)

    async def get_target(self, mission_id: int, target_id: int) -> Target | None:
        stmt = select(Target).where(
            Target.mission_id == mission_id, Target.id == target_id
        )
        return await self.session.scalar(stmt)
    
    async def get_active_cat_mission(self, cat_id: int) -> Mission | None:
        stmt = select(Mission).where(
            Mission.cat_id == cat_id, Mission.is_complete == False)
        return await self.session.scalar(stmt)

