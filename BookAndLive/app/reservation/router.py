from fastapi import APIRouter, HTTPException, Depends
from app.reservation.model import *

from bson import ObjectId, Timestamp


reservation_router = APIRouter(
    prefix="/reservations",
    tags=["reservations"],
    responses={404: {"description": "Not found"}},
)


@reservation_router.get(
    "/{reservation_id}",
    response_description="Single reservation with given ID",
    response_model=ReservationSchema
)
async def reservation_by_id(reservation_id: str):
    if not ObjectId.is_valid(reservation_id):
        raise HTTPException(status_code=400, detail='Bad Request')
    raise HTTPException(status_code=404, detail=f'Reservation with ID : {reservation_id} not found')


@reservation_router.post(
    "/",
    response_description="Added reservation ID",
    response_model=str
)
async def reservation_add(reservation: ReservationSchema):
    raise HTTPException(status_code=404, detail=f'Reservation with ID : already exists')


@reservation_router.put(
    "/{reservation_id}",
    response_description="Updated reservation",
    response_model=UpdateReservationSchema
)
async def reservation_update(reservation_id: str,
                             reservation_upd: UpdateReservationSchema):
    if not ObjectId.is_valid(reservation_id):
        raise HTTPException(status_code=400, detail='Bad Request')
    raise HTTPException(status_code=404, detail=f'Reservation with ID : {reservation_id} not found')


@reservation_router.get(
    "/client/{client_id}",
    response_description="All reservations for given client",
    response_model=list[ReservationSchema]
)
async def reservations_by_client_id(client_id: str):
    if not ObjectId.is_valid(client_id):
        raise HTTPException(status_code=400, detail='Bad Request')
    raise HTTPException(status_code=404, detail=f'No such client with ID: {client_id}')


@reservation_router.get(
    "/from/{time_from}/to/{time_to}",
    response_description="All reservations in the given period",
    response_model=list[ReservationSchema]
)
async def reservations_from_to(time_from: datetime,
                               time_to: datetime):
    raise HTTPException(status_code=404, detail=f'No reservations in this period: from {time_from}, to {time_to}')


@reservation_router.get(
    "/booking_time/{booking_time}",
    response_description="All reservations in the given period",
    response_model=list[ReservationSchema]
)
async def reservations_by_booking_time(booking_time: datetime):
    raise HTTPException(status_code=404, detail=f'No reservations for this date: {booking_time}')


@reservation_router.get(
    "/rooms/{room_id}",
    response_description="All reservations for this room",
    response_model=list[ReservationSchema]
)
async def reservations_by_room_id(room_id: str):
    if not ObjectId.is_valid(room_id):
        raise HTTPException(status_code=400, detail='Bad Request')
    raise HTTPException(status_code=404, detail=f'No such room with ID: {room_id}')
