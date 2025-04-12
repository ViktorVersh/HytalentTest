"""
Определяем схемы (Pydantic модели) для работы с данными по столикам.
"""
from typing import Optional
from pydantic import BaseModel


class TableBase(BaseModel):
    name: str
    seats: int
    location: Optional[str] = "Центр зала"


class TableCreate(TableBase):
    pass


class TableRead(TableBase):
    id: int


class TableUpdate(BaseModel):
    name: Optional[str] = None
    seats: Optional[int] = None
    location: Optional[str] = None
