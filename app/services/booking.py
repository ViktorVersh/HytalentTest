from datetime import datetime, timedelta
from sqlmodel import Session, select
from fastapi import HTTPException, status
from app.models.reservation import Reservation


class BookingService:
    @staticmethod
    def is_table_available(session: Session, table_id: int,
                           reservation_time: datetime, duration: int) -> bool:
        end_time = reservation_time + timedelta(minutes=duration)

        conflicting = session.exec(
            select(Reservation)
            .where(Reservation.table_id == table_id)
            .where(
                (Reservation.reservation_time < end_time) &
                (Reservation.reservation_time +
                 timedelta(minutes=Reservation.duration_minutes) > reservation_time)
            )
        ).first()

        return not conflicting

    @classmethod
    def create_reservation(cls, session: Session, reservation_data: dict):
        if not cls.is_table_available(session,
                                      reservation_data["table_id"],
                                      reservation_data["reservation_time"],
                                      reservation_data["duration_minutes"]):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Столик уже забронирован на это время"
            )

        reservation = Reservation(**reservation_data)
        session.add(reservation)
        session.commit()
        session.refresh(reservation)
        return reservation
