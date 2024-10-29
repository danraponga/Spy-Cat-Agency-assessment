from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_cat_repository, get_mission_repository
from app.api.schemas.missions import (
    CreateMissionRequest,
    MissionId,
    MissionResponse,
    TargetResponse,
    TargetUpdate,
)
from app.db.repositories.cat_repository import CatRepository
from app.db.repositories.mission_respository import MissionRepository

missions_router = APIRouter()


@missions_router.post("", response_model=MissionResponse)
async def create_mission(
    data: CreateMissionRequest,
    cat_repository: CatRepository = Depends(get_cat_repository),
    mission_repository: MissionRepository = Depends(get_mission_repository),
):
    if not 1 <= len(data.targets) <=3:
        raise HTTPException(status_code=400, detail="Mission must have 1 to 3 targets")
    
    if data.cat_id and not await cat_repository.get(data.cat_id):
        return HTTPException(status_code=404, detail="Cat not found")

    mission = await mission_repository.create({"cat_id": data.cat_id})

    target_schemas = []
    for target in data.targets:
        target_dict = target.model_dump()
        target_dict.update({"mission_id": mission.id})
        target_model = await mission_repository.create_target(target_dict)

        target_schemas.append(
            TargetResponse.model_validate(target_model, from_attributes=True)
        )

    await mission_repository._commit()
    return MissionResponse(
        id=mission.id,
        cat_id=mission.cat_id,
        is_complete=mission.is_complete,
        targets=target_schemas,
    )


@missions_router.get("", response_model=list[MissionResponse])
async def get_missions_list(
    limit: int = 10,
    mission_repository: MissionRepository = Depends(get_mission_repository),
):
    return await mission_repository.get_list(limit)


@missions_router.get("/{mission_id}", response_model=MissionResponse)
async def get_mission(
    mission_id: int,
    mission_repository: MissionRepository = Depends(get_mission_repository),
):
    mission = await mission_repository.get(mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission


@missions_router.patch("/{mission_id}/assign", status_code=204)
async def assign_cat_to_mission(
    cat_id: int,
    mission_id: int,
    cat_repository: CatRepository = Depends(get_cat_repository),
    mission_repository: MissionRepository = Depends(get_mission_repository),
):
    cat = await cat_repository.get(cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    
    if await mission_repository.get_active_cat_mission(cat_id):
        raise HTTPException(status_code=409, detail="Cat already has active mission")

    mission = await mission_repository.get(mission_id)
    if not mission:
        raise HTTPException(status=404, detail="Mission not found")
    if mission.cat_id:
        raise HTTPException(
            status_code=409, detail="Another cat already assigned to this mission"
        )

    mission.cat_id = cat_id
    await mission_repository._commit()


@missions_router.delete("/{mission_id}/delete", status_code=204)
async def delete_misssion(
    mission_id: int,
    mission_repository: MissionRepository = Depends(get_mission_repository),
):
    mission = await mission_repository.get(mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    if mission.cat_id:
        raise HTTPException(status_code=400, detail="Mission already assigned")

    await mission_repository._delete(mission)
    await mission_repository._commit()


@missions_router.patch(
    "/{mission_id}/targets/{target_id}", response_model=TargetResponse
)
async def update_target(
    mission_id: int,
    target_id: int,
    data: TargetUpdate,
    mission_repository: MissionRepository = Depends(get_mission_repository),
):
    if not data.is_complete and not data.notes:
        raise HTTPException(status_code=400, detail="No data provided")

    target = await mission_repository.get_target(mission_id, target_id)
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")

    mission = await mission_repository.get(mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    if target.is_complete or mission.is_complete:
        raise HTTPException(
            status_code=400, detail="Target or mission already completed"
        )

    target.is_complete = data.is_complete or target.is_complete
    target.notes = data.notes or target.notes

    await mission_repository._commit()

    for target in mission.targets:
        if not target.is_complete:
            return target

    # If all targets are completed - set mission completed
    mission.is_complete = True
    await mission_repository._commit()
    return target
