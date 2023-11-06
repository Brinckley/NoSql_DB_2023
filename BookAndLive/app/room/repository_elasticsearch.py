import os
from fastapi import Depends
from datetime import datetime

from elasticsearch import AsyncElasticsearch

from app.repository.elasticsearch_utils import get_es_client
from app.room.model import RoomSchema, UpdateRoomSchema


class RoomSearchRepository:
    _elasticsearch_client: AsyncElasticsearch
    _elasticsearch_index: str

    def __int__(self, elasticsearch_client: AsyncElasticsearch, index: str):
        self._elasticsearch_client = elasticsearch_client
        self._elasticsearch_index = index

    async def create(self, room_id: str, room: RoomSchema):
        await self._elasticsearch_client.create(index=self._elasticsearch_index, id=room_id,
                                                document=dict(room))

    async def update(self, room_id: str, room: UpdateRoomSchema):
        await self._elasticsearch_client.update(index=self._elasticsearch_index, id=room_id,
                                                doc=dict(room))

    async def delete(self, room_id: str):
        await self._elasticsearch_client.delete(index=self._elasticsearch_index, id=room_id)

    async def find_by_attributes(self, attributes: str):  # logic not written yet
        return

    async def find_by_country(self, country: str):  # logic not written yet
        return

    async def find_by_city(self, city: str):  # logic not written yet
        return

    @staticmethod
    def es_client_factory(elasticsearch_client: AsyncElasticsearch = Depends(get_es_client)):
        elasticsearch_index = os.getenv('ELASTICSEARCH_INDEX')
        return RoomSearchRepository(elasticsearch_client, elasticsearch_index)