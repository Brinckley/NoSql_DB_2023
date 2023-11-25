from fastapi import Depends

from motor.motor_asyncio import AsyncIOMotorCollection

from app.room.model import *
from app.repository.mongo_utils import get_mongo_client


class RoomMongoRepository:
    mongo_collection: AsyncIOMotorCollection

    @staticmethod
    def mongo_client_factory(mongo_collection: AsyncIOMotorCollection = Depends(get_mongo_client)):
        return RoomMongoRepository(mongo_collection)

    def get_all_rooms(self) -> list:
        return [RoomSchema()]

    def get_room(self,
                 room_id: str) -> RoomSchema:
        return RoomSchema()

    def add_room(self,
                 room: RoomSchema) -> str:
        return ""

    def update_room(self,
                    room_id: str,
                    room: UpdateRoomSchema) -> RoomSchema:
        return RoomSchema()

    def delete_room(self,
                    room_id: str) -> RoomSchema:
        return RoomSchema()