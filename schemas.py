from pydantic import BaseModel
from typing import Optional

class BookBase(BaseModel):
    title: str
    description: str
    author: str
    year: int


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None


class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True
