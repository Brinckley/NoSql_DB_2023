from fastapi import Depends

from motor.motor_asyncio import AsyncIOMotorCollection

from app.room.model import *
from app.repository.mongo_utils import get_db_collection


class RoomMongoRepository:
    mongo_collection: AsyncIOMotorCollection

    def __init__(self, db_collection: AsyncIOMotorCollection):
        self._db_collection = db_collection

    @staticmethod
    def mongo_client_factory(mongo_collection: AsyncIOMotorCollection = Depends(get_db_collection)):
        return RoomMongoRepository(mongo_collection)

    async def get_all_rooms(self) -> list[RoomSchema]:
        return [RoomSchema()]

    async def get_room_by_id(self,
                 room_id: str) -> RoomSchema:
        return RoomSchema()

    async def add_room(self,
                 room: UpdateRoomSchema) -> str:
        return ""

    async def update_room(self,
                    room_id: str,
                    room: UpdateRoomSchema) -> RoomSchema:
        return RoomSchema()

    async def delete_room(self,
                    room_id: str) -> RoomSchema:
        return RoomSchema()
