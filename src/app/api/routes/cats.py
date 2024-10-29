import httpx
from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_cat_repository
from app.api.schemas.cats import CatResponse, CatUpdate, CreateCatRequest
from app.db.repositories.cat_repository import CatRepository

cats_router = APIRouter()


@cats_router.post("", response_model=CatResponse)
async def create_cat(
    data: CreateCatRequest, cat_repository: CatRepository = Depends(get_cat_repository)
):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.thecatapi.com/v1/breeds/search?name={data.breed}"
        )
        response_data = response.json()

    if not response_data:
        raise HTTPException(status_code=400, detail="Invalid breed")

    cat = await cat_repository.create(data.model_dump())
    await cat_repository._commit()
    return cat


@cats_router.get("", response_model=list[CatResponse])
async def get_cats_list(
    limit: int = 10, cat_repository: CatRepository = Depends(get_cat_repository)
):
    return await cat_repository.get_list(limit)


@cats_router.get("/{cat_id}", response_model=CatResponse)
async def get_cat(
    cat_id: int, cat_repository: CatRepository = Depends(get_cat_repository)
):
    cat = await cat_repository.get(cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    return cat


@cats_router.patch("/{cat_id}", response_model=CatResponse)
async def update_cat(
    cat_id: int,
    data: CatUpdate,
    cat_repository: CatRepository = Depends(get_cat_repository),
):
    cat = await cat_repository.get(cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")

    cat.salary = data.salary
    await cat_repository._commit()

    return cat


@cats_router.delete("/{cat_id}", status_code=204)
async def delete_cat(
    cat_id: int, cat_repository: CatRepository = Depends(get_cat_repository)
):
    cat = await cat_repository.get(cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")

    await cat_repository._delete(cat)
    await cat_repository._commit()
