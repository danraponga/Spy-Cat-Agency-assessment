from pydantic import BaseModel


class CatBase(BaseModel):
    name: str
    years_of_experience: int
    breed: str
    salary: int


class CatId(BaseModel):
    id: int


class CreateCatRequest(CatBase):
    pass


class CatResponse(CatId, CatBase):
    pass


class CatUpdate(BaseModel):
    salary: int
