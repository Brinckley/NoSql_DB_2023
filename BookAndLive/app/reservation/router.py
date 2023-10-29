from fastapi import APIRouter, HTTPException
from app.reservation.model import *
from app.reservation.repository_mongo import *


reservation_router = APIRouter(
    prefix="/reservations",
    tags=["reservations"],
    responses={404: {"description": "Not found"}},
)


# Want to look closely on concrete reservation by its id
@reservation_router.get(
    "/{reservation_id}",
    response_description="Get a single reservation",
    response_model=ReservationSchema
)
async def reservation_by_id(reservation_id: str):
    if (reservation := await get_reservation(reservation_id)) is not None:
        return reservation
    raise HTTPException(status_code=404, detail=f'Reservation with ID : {reservation_id} not found')


# Create another reservation
@reservation_router.post(
    "/",
    response_description="Create a single reservation"
)
async def reservation_add(reservation: ReservationSchema):
    if (reservation := await get_reservation(reservation.id)) is not None:
        add_reservation(reservation)


# Update the reservation data
@reservation_router.put(
    "/{reservation_id}",
    response_description="Update a single reservation",
    response_model=ReservationSchema
)
async def reservation_update(reservation_id: str, reservation: ReservationSchema):
    if (reservation := await get_reservation(reservation_id)) is not None:
        update_reservation(reservation_id, reservation)
    raise HTTPException(status_code=404, detail=f'Reservation with ID : {reservation_id} not found')