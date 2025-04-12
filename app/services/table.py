from sqlmodel import Session, select
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import datetime, timedelta

from app.models.table import Table
from app.models.reservation import Reservation
from app.schemas.table import TableCreate, TableUpdate


class TableService:
    @staticmethod
    def create_table(session: Session, table_data: TableCreate) -> Table:
        """Создание нового столика с валидацией"""
        # Проверяем уникальность имени столика
        existing_table = session.exec(
            select(Table).where(Table.name == table_data.name)
        ).first()

        if existing_table:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Столик с именем '{table_data.name}' уже существует"
            )

        # Проверяем корректность количества мест
        if table_data.seats <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Количество мест должно быть положительным числом"
            )

        db_table = Table(**table_data.dict())
        session.add(db_table)
        session.commit()
        session.refresh(db_table)
        return db_table

    @staticmethod
    def get_table_by_id(session: Session, table_id: int) -> Table:
        """Получение столика по ID"""
        table = session.get(Table, table_id)
        if not table:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Столик с ID {table_id} не найден"
            )
        return table

    @staticmethod
    def get_all_tables(session: Session, skip: int = 0, limit: int = 100) -> List[Table]:
        """Получение списка всех столиков с пагинацией"""
        return session.exec(select(Table).offset(skip).limit(limit)).all()

    @staticmethod
    def update_table(session: Session, table_id: int, table_data: TableUpdate) -> Table:
        """Обновление данных столика"""
        db_table = TableService.get_table_by_id(session, table_id)

        # Проверяем уникальность имени, если оно передано для обновления
        if table_data.name is not None:
            existing_table = session.exec(
                select(Table).where(Table.name == table_data.name)
            ).first()
            if existing_table and existing_table.id != table_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Столик с именем '{table_data.name}' уже существует"
                )

        # Обновляем только переданные поля
        update_data = table_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_table, key, value)

        session.add(db_table)
        session.commit()
        session.refresh(db_table)
        return db_table

    @staticmethod
    def delete_table(session: Session, table_id: int) -> None:
        """Удаление столика с проверкой на активные брони"""
        db_table = TableService.get_table_by_id(session, table_id)

        # Проверяем наличие активных броней
        active_reservations = session.exec(
            select(Reservation)
            .where(Reservation.table_id == table_id)
            .where(Reservation.reservation_time >= datetime.now())
        ).first()

        if active_reservations:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Нельзя удалить столик с активными бронями"
            )

        session.delete(db_table)
        session.commit()

    @staticmethod
    def get_available_tables(
            session: Session,
            start_time: datetime,
            duration_minutes: int,
            min_seats: Optional[int] = None,
            location: Optional[str] = None
    ) -> List[Table]:
        """Поиск доступных столиков по заданным параметрам"""
        end_time = start_time + timedelta(minutes=duration_minutes)

        # Базовый запрос для поиска столиков
        query = select(Table)

        # Фильтр по количеству мест
        if min_seats is not None:
            query = query.where(Table.seats >= min_seats)

        # Фильтр по расположению
        if location is not None:
            query = query.where(Table.location == location)

        # Получаем все подходящие столики
        tables = session.exec(query).all()

        # Фильтруем столики по доступности
        available_tables = []
        for table in tables:
            # Проверяем наличие конфликтующих броней
            conflicting_reservation = session.exec(
                select(Reservation)
                .where(Reservation.table_id == table.id)
                .where(
                    (Reservation.reservation_time < end_time) &
                    (Reservation.reservation_time +
                     timedelta(minutes=Reservation.duration_minutes) > start_time)
                )
            ).first()

            if not conflicting_reservation:
                available_tables.append(table)

        return available_tables