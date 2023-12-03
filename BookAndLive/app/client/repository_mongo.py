from __future__ import annotations

from fastapi import Depends

from motor.motor_asyncio import AsyncIOMotorCollection

from app.client.model import *
from app.repository.mongo_utils import *


class ClientMongoRepository:
    _mongo_collection: AsyncIOMotorCollection

    def __init__(self, mongo_collection: AsyncIOMotorCollection):
        self._mongo_collection = mongo_collection

    @staticmethod
    def mongo_client_factory(mongo_collection: AsyncIOMotorCollection = Depends(get_db_collection)):
        return ClientMongoRepository(mongo_collection)

    async def get_client(self,
                         client_id: str) -> ClientSchema | None:
        print(f'Get client {client_id} from mongo')
        db_client = await self._mongo_collection.find_one(get_filter(client_id))
        return map_client(db_client)

    async def add_client(self,
                         client: ClientSchema) -> str:
        insert_result = await self._mongo_collection.insert_one(dict(client))
        return str(insert_result.inserted_id)

    async def update_client(self,
                            client_id: str,
                            client: UpdateClientSchema) -> ClientSchema | None:
        db_client = await self._mongo_collection.find_one_and_replace(get_filter(client_id), dict(client))
        return map_client(db_client)

    async def delete_client(self,
                            client_id: str) -> ClientSchema | None:
        db_client = await self._mongo_collection.find_one_and_delete(get_filter(client_id))
        return map_client(db_client)