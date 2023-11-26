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
    "/",
    response_description="All rooms available",
    response_model=list[RoomSchema]
)
async def list_available_rooms(es_repository: RoomEsRepository = Depends(RoomEsRepository.es_client_factory)):
    if (rooms := await es_repository.find_available()) is not None:
        return {"rooms": rooms}
    raise HTTPException(status_code=404, detail=f'No available rooms')


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


@room_router.get(
    "/city/{city_name}",
    response_description="All rooms available in the given city",
    response_model=list[RoomSchema]
)
async def list_available_rooms_city(city_name: str,
                                    es_repository: RoomEsRepository = Depends(RoomEsRepository.es_client_factory)):
    if (rooms := await es_repository.find_by_city(city_name)) is not None:
        return {"rooms": rooms}
    raise HTTPException(status_code=404, detail=f'No available rooms in the given city: {city_name}')


@room_router.get(
    "/country/{country_name}",
    response_description="All rooms available in the given country",
    response_model=list[RoomSchema]
)
async def list_available_rooms_country(country_name: str,
                                       es_repository: RoomEsRepository = Depends(RoomEsRepository.es_client_factory)):
    if (rooms := await es_repository.find_by_country(country_name)) is not None:
        return {"rooms": rooms}
    raise HTTPException(status_code=404, detail=f'No available rooms in the given country: {country_name}')


@room_router.get(
    "/attributes/{attributes_list}",
    response_description="All rooms available in the given country",
    response_model=list[RoomSchema]
)
async def list_available_rooms_attributes(attributes_list: str,
                                          es_repository: RoomEsRepository = Depends(RoomEsRepository.es_client_factory)):
    if (rooms := await es_repository.find_by_attributes(attributes_list)) is not None:
        return {"rooms": rooms}
    raise HTTPException(status_code=404, detail=f'No available rooms in the given attributes: {attributes_list}')


