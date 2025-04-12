from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from app.models.table import Table


class Reservation(SQLModel, table=True):
    """
    Определение модели бронирования стола
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_name: str
    table_id: int = Field(foreign_key="table.id")
    reservation_time: datetime
    duration_minutes: int = Field(default=60, gt=0)

    table: Table = Relationship()
