from typing import Literal

from pydantic import BaseModel, Field


class BaseTarget(BaseModel):
    name: str
    country: str
    notes: str | None


class TargetResponse(BaseTarget):
    id: int
    is_complete: bool


class TargetUpdate(BaseModel):
    is_complete: Literal[True] | None
    notes: str | None


class BaseMission(BaseModel):
    cat_id: int | None = Field(examples=[None])


class MissionId(BaseModel):
    id: int


class CreateMissionRequest(BaseMission):
    targets: list[BaseTarget]


class MissionResponse(MissionId, BaseMission):
    is_complete: bool
    targets: list[TargetResponse]
