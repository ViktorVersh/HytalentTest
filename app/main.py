from fastapi import FastAPI
from fastapi.logger import logger

from app.routers import table, reservation

app = FastAPI()

app.include_router(table.router)
app.include_router(reservation.router)


@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в REST API по бронированию столиков!"}


if "__main__" == __name__:
    import uvicorn

    # Конфигурация сервера
    server_config = {
        "app": "main:app",
        "host": "127.0.0.1",
        "port": 8000,
        "reload": True,
        "log_level": "info"
    }

    logger.info("Starting server...")
    uvicorn.run(**server_config)
