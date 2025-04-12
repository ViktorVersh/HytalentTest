from fastapi.testclient import TestClient
from datetime import datetime, timedelta

from sqlmodel import Session

from app.main import app
from app.models.table import Table

client = TestClient(app)


def test_create_reservation(session: Session):
    """
    Тест для создания новой брони
    :return:
    """
    # Сначала создаем тестовый столик
    table = Table(name="Test Table", seats=4, location="Test Location")
    session.add(table)
    session.commit()

    # Создаем бронь
    response = client.post(
        "/reservations/",
        json={
            "customer_name": "Test User",
            "table_id": table.id,
            "reservation_time": (datetime.now() + timedelta(days=1)).isoformat(),
            "duration_minutes": 60
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["customer_name"] == "Test User"
    assert data["table_id"] == table.id
