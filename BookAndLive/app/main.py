from fastapi import FastAPI
from app.room.router import room_router
from app.client.router import client_router
from app.reservation.router import reservation_router
from app.repository.utils import *

app = FastAPI(
    title="Book & Live"
)

app.add_event_handler("startup", startup_handling)
app.add_event_handler("shutdown", shutdown_handling)

app.include_router(room_router)
app.include_router(client_router)
app.include_router(reservation_router)
