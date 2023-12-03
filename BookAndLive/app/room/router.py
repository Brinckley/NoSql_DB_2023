from fastapi import APIRouter, HTTPException, Body

from bson import ObjectId
from app.room.model import *

room_router = APIRouter(
    prefix="",
    tags=["rooms"],
    responses={404: {"description": "Not found"}},
)


# Home page, listing all available rooms.
@room_router.get(
    "/",
    response_description="All rooms available",
    response_model=list[RoomSchema]
)
async def list_available_rooms():
    raise HTTPException(status_code=404, detail=f'No available rooms')


@room_router.get(
    "/{room_id}",
    response_description="Get a single room by id",
    response_model=RoomSchema
)
async def room_by_id(room_id: str):
    if not ObjectId.is_valid(room_id):
        raise HTTPException(status_code=400, detail='Bad Request')
    raise HTTPException(status_code=404, detail=f'Room with ID : {room_id} not found')


@room_router.post(
    "/",
    response_description="New room id",
    response_model=int
)
async def room_add(room: RoomSchema):
    raise HTTPException(status_code=404, detail=f'Room with ID : already exists')


@room_router.put(
    "/{room_id}",
    response_description="Updated a single room",
    response_model=RoomSchema
)
async def room_update(room_id: str,
                      room: UpdateRoomSchema):
    if not ObjectId.is_valid(room_id):
        raise HTTPException(status_code=400, detail='Bad Request')

    raise HTTPException(status_code=404, detail=f'Room with ID : {room_id} already exists')


@room_router.get(
    "/city/{city_name}",
    response_description="All rooms available in the given city",
    response_model=list[RoomSchema]
)
async def list_available_rooms_city(city_name: str):
    raise HTTPException(status_code=404, detail=f'No available rooms in the given city: {city_name}')


@room_router.get(
    "/country/{country_name}",
    response_description="All rooms available in the given country",
    response_model=list[RoomSchema]
)
async def list_available_rooms_country(country_name: str):
    raise HTTPException(status_code=404, detail=f'No available rooms in the given country: {country_name}')


@room_router.get(
    "/attributes/{attributes_list}",
    response_description="All rooms available in the given country",
    response_model=list[RoomSchema]
)
async def list_available_rooms_attributes(attributes_list: str):
    raise HTTPException(status_code=404, detail=f'No available rooms in the given attributes: {attributes_list}')
