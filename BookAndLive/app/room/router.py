from fastapi import APIRouter, HTTPException, Body
from app.room.repository_mongo import *
from app.room.model import *

room_router = APIRouter(
    prefix="",
    tags=["rooms"],
    responses={404: {"description": "Not found"}},
)


# Home page, listing all available rooms.
@room_router.get(
    "/",
    response_description="List all students",
    response_model=list[RoomSchema]
)
async def list_rooms():
    rooms = await get_all_rooms()
    return rooms


# Want to look closely on concrete room by its id
@room_router.get(
    "/{room_id}",
    response_description="Get a single room",
    response_model=RoomSchema
)
async def room_by_id(room_id: str):
    if (room := await get_room(room_id)) is not None:
        return room
    raise HTTPException(status_code=404, detail=f'Room with ID : {room_id} not found')


# Create another room
@room_router.post(
    "/",
    response_description="Create a single room"
)
async def room_add(room: RoomSchema):
    if (room := await get_room(room.id)) is not None:
        add_room(room)


# Update the rooms data
@room_router.put(
    "/{room_id}",
    response_description="Update a single room",
    response_model=RoomSchema
)
async def room_update(room_id: str, room: RoomSchema):
    if (room := await get_room(room_id)) is not None:
        update_room(room_id, room)