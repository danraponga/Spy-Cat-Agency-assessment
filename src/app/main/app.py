from fastapi import FastAPI

from app.api.root import api_router


def get_app() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router)
    return app
