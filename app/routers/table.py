from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.services.table import TableService
from app.schemas.table import TableCreate, TableRead, TableUpdate
from app.db import get_session

router = APIRouter(prefix="/tables", tags=["tables"])


#  Создание столика
@router.post("/", response_model=TableRead, status_code=status.HTTP_201_CREATED)
async def create_table(table: TableCreate, session: Session = Depends(get_session)):
    return TableService.create_table(session, table)


#  Получение списка всех столиков
@router.get("/", response_model=list[TableRead])
async def read_tables(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    return TableService.get_all_tables(session, skip, limit)


#  Получение информации о столике по его ID
@router.get("/{table_id}", response_model=TableRead)
async def read_table(table_id: int, session: Session = Depends(get_session)):
    return TableService.get_table_by_id(session, table_id)


#  Изменение столика с указанным ID
@router.patch("/{table_id}", response_model=TableRead)
async def update_table(
        table_id: int,
        table: TableUpdate,
        session: Session = Depends(get_session)
):
    return TableService.update_table(session, table_id, table)

#  Удаление столика с указанным ID
@router.delete("/{table_id}")
async def delete_table(table_id: int, session: Session = Depends(get_session)):
    TableService.delete_table(session, table_id)
    return {"message": "Столик успешно удален"}
