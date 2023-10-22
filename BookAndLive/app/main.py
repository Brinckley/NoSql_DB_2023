from fastapi import FastAPI
from app.room.router import room_router
from app.client.router import client_router
from app.reservation.router import reservation_router

app = FastAPI(
    title="Book & Live"
)
app.include_router(room_router)
app.include_router(client_router)
app.include_router(reservation_router)


@app.on_event("startup")
async def startup():
    # getting some connection string from environment (docker)
    # connecting to db
    # same with es
    print("startup")


@app.on_event("shutdown")
async def shutdown():
    # graceful shutdown
    print("shutdown")

