from fastapi import APIRouter

from app.api.routes.cats import cats_router
from app.api.routes.missions import missions_router

api_router = APIRouter(prefix="/api")
api_router.include_router(cats_router, prefix="/cats", tags=["Cats"])
api_router.include_router(missions_router, prefix="/missions", tags=["Missions"])


@api_router.get("/healtcheck")
async def check_health() -> dict:
    return {"status": "healthy"}
