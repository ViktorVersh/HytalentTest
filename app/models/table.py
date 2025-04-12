from sqlmodel import SQLModel, Field
from typing import Optional


class Table(SQLModel, table=True):
    """
    Определяет таблицу со столиками в базе данных
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    seats: int = Field(gt=0, description="Количество мест")
    location: str = Field(default="Центр зала", description="Расположение столика")
