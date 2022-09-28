from pydantic import BaseModel


class File(BaseModel):
    id: int
    name: str
    size: int

    class Config:
        orm_mode = True
