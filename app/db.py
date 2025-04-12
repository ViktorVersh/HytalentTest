from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.engine import Engine
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/restaurant")

engine: Engine = create_engine(DATABASE_URL)


def get_session():
    """
    Create a database session
    :return:
    """
    with Session(engine) as session:
        yield session


def init_db():
    """
    Create all tables
    :return:
    """
    SQLModel.metadata.create_all(engine)
