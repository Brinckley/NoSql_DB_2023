from __future__ import annotations


from motor.motor_asyncio import AsyncIOMotorCollection

from models.client_model import *
from models.room_model import *
from models.reservation_model import *
from repository.utils.mongo_utils import *


class ClientMongoRepository:
    _mongo_collection: AsyncIOMotorCollection

    def __init__(self, mongo_collection: AsyncIOMotorCollection):
        self._mongo_collection = mongo_collection

    async def add_client(self,
                         client: UpdateClientSchema) -> str:
        insert_result = await self._mongo_collection.insert_one(dict(client))
        print(f'App client {insert_result.inserted_id} from mongo')
        return str(insert_result.inserted_id)


class ReservationMongoRepository:
    _mongo_collection: AsyncIOMotorCollection

    def __init__(self, mongo_collection: AsyncIOMotorCollection):
        self._mongo_collection = mongo_collection

    async def add_reservation(self,
                              reservation: UpdateReservationSchema) -> str:
        insert_result = await self._mongo_collection.insert_one(dict(reservation))
        print(f'Add reservation {insert_result.inserted_id} from mongo')
        return str(insert_result.inserted_id)


class RoomMongoRepository:
    _mongo_collection: AsyncIOMotorCollection

    def __init__(self, mongo_collection: AsyncIOMotorCollection):
        self._mongo_collection = mongo_collection

    async def add_room(self,
                       room: UpdateRoomSchema) -> str:
        insert_result = await self._mongo_collection.insert_one(dict(room))
        print(f'Add room {insert_result.inserted_id} from mongo')
        return str(insert_result.inserted_id)
