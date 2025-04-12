"""
Определяем схемы (Pydantic модели) для работы с данными по бронированию.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ReservationCreate(BaseModel):
    customer_name: str
    table_id: int
    reservation_time: datetime
    duration_minutes: int = 60


class ReservationRead(BaseModel):
    id: int
    customer_name: str
    table_id: int
    reservation_time: datetime
    duration_minutes: int
