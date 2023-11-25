from fastapi import APIRouter, HTTPException, Body
from app.room.repository_mongo import *
from bson import ObjectId
from app.room.repository_elasticsearch import *
from app.room.model import *

room_router = APIRouter(
    prefix="",
    tags=["rooms"],
    responses={404: {"description": "Not found"}},
)


# Home page, listing all available rooms.
@room_router.get(
    "/from/{time_from}/to/{time_to}",
    response_description="All rooms available at certain period",
    response_model=list[RoomSchema]
)
async def list_available_rooms(time_from: datetime,
                               time_to: datetime,
                               es_repository: RoomEsRepository = Depends(RoomEsRepository.es_client_factory)):
    if (rooms := await es_repository.find_available_in_range(time_from, time_to)) is not None:
        return {"rooms": rooms}
    raise HTTPException(status_code=404, detail=f'Room in period from : {time_from} to {time_to}')


@room_router.get(
    "/{room_id}",
    response_description="Get a single room by id",
    response_model=RoomSchema
)
async def room_by_id(room_id: str,
                     mongo_repository: RoomMongoRepository = Depends(RoomMongoRepository.mongo_client_factory)):
    if not ObjectId.is_valid(room_id):
        raise HTTPException(status_code=400, detail='Bad Request')

    if (room := await mongo_repository.get_room(room_id)) is not None:
        return {"room": room}
    raise HTTPException(status_code=404, detail=f'Room with ID : {room_id} not found')


@room_router.post(
    "/",
    response_description="New room id",
    response_model=int
)
async def room_add(room: RoomSchema,
                   mongo_repository: RoomMongoRepository = Depends(RoomMongoRepository.mongo_client_factory),
                   es_repository: RoomEsRepository = Depends(RoomEsRepository.es_client_factory)):
    if (room_id := await mongo_repository.add_room(room)) is not None:
        await es_repository.create(room_id, room)
        return {"room_id": room_id}
    raise HTTPException(status_code=404, detail=f'Room with ID : {room_id} already exists')


@room_router.put(
    "/{room_id}",
    response_description="Updated a single room",
    response_model=RoomSchema
)
async def room_update(room_id: str,
                      room: UpdateRoomSchema,
                      mongo_repository: RoomMongoRepository = Depends(RoomMongoRepository.mongo_client_factory),
                      es_repository: RoomEsRepository = Depends(RoomEsRepository.es_client_factory)):
    if not ObjectId.is_valid(room_id):
        raise HTTPException(status_code=400, detail='Bad Request')

    if (room_upd := await mongo_repository.update_room(room_id, room)) is not None:
        await es_repository.update(room_id, room)
        return {"room_upd": room_upd}
    raise HTTPException(status_code=404, detail=f'Room with ID : {room_id} already exists')

