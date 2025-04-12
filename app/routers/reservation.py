"""
Функционал для работы с бронированием
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.models.reservation import Reservation
from app.services.booking import BookingService
from app.schemas.reservation import (
    ReservationCreate,
    ReservationRead
)
from app.db import get_session

router = APIRouter(prefix="/reservations", tags=["reservations"])


#  Добавление бронирования
@router.post("/", response_model=ReservationRead)
async def create_reservation(
        reservation: ReservationCreate,
        session: Session = Depends(get_session)
):
    return BookingService.create_reservation(session, reservation.dict())


#  Получение всех бронирований
@router.get("/", response_model=list[ReservationRead])
async def read_reservations(session: Session = Depends(get_session)):
    reservations = session.exec(select(Reservation)).all()
    return reservations


#  Удаление конкретного бронирования по id
@router.delete("/{reservation_id}")
async def delete_reservation(
        reservation_id: int,
        session: Session = Depends(get_session)
):
    reservation = session.get(Reservation, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Бронь не найдена")
    session.delete(reservation)
    session.commit()
    return {"ok": True}
