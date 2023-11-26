import os
from fastapi import Depends

from elasticsearch import AsyncElasticsearch

from app.repository.elasticsearch_utils import get_es_client
from app.client.model import ClientSchema, UpdateClientSchema


class ClientEsRepository:
    _elasticsearch_client: AsyncElasticsearch
    _elasticsearch_index: str

    @staticmethod
    def es_client_factory(elasticsearch_client: AsyncElasticsearch = Depends(get_es_client)):
        elasticsearch_index = os.getenv('ELASTICSEARCH_INDEX')
        return ClientEsRepository(elasticsearch_client, elasticsearch_index)

    def __int__(self, elasticsearch_client: AsyncElasticsearch, index: str):
        self._elasticsearch_client = elasticsearch_client
        self._elasticsearch_index = index

    async def create(self, client_id: str, client: ClientSchema):
        await self._elasticsearch_client.create(index=self._elasticsearch_index, id=client_id, document=dict(client))

    async def update(self, client_id: str, client: UpdateClientSchema):
        await self._elasticsearch_client.update(index=self._elasticsearch_index, id=client_id, doc=dict(client))

    async def delete(self, client_id: str):
        await self._elasticsearch_client.delete(index=self._elasticsearch_index, id=client_id)