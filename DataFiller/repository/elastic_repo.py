import os

from elasticsearch import AsyncElasticsearch

from repository.utils.elasticsearch_utils import get_elasticsearch_client
from models.client_model import *
from models.room_model import *
from models.reservation_model import *


class ClientEsRepository:
    _elasticsearch_client: AsyncElasticsearch
    _elasticsearch_index: str

    def __init__(self, elasticsearch_client: AsyncElasticsearch):
        self._elasticsearch_client = elasticsearch_client
        self._elasticsearch_index = os.getenv('ELASTICSEARCH_INDEX_CLIENT')

    async def create(self, client_id: str, client: UpdateClientSchema):
        await self._elasticsearch_client.create(index=self._elasticsearch_index, id=client_id, document=dict(client))


class ReservationEsRepository:
    _elasticsearch_client: AsyncElasticsearch
    _elasticsearch_index: str

    def __init__(self, elasticsearch_client: AsyncElasticsearch):
        self._elasticsearch_client = elasticsearch_client
        self._elasticsearch_index = os.getenv('ELASTICSEARCH_INDEX_RESERVATION')

    async def create(self, reservation_id: str, reservation: UpdateReservationSchema):
        await self._elasticsearch_client.create(index=self._elasticsearch_index, id=reservation_id,
                                                document=dict(reservation))


class RoomEsRepository:
    _elasticsearch_client: AsyncElasticsearch
    _elasticsearch_index: str

    def __init__(self, elasticsearch_client: AsyncElasticsearch):
        self._elasticsearch_client = elasticsearch_client
        self._elasticsearch_index = os.getenv('ELASTICSEARCH_INDEX_ROOM')

    async def create(self, room_id: str, room: UpdateRoomSchema):
        await self._elasticsearch_client.create(index=self._elasticsearch_index, id=room_id,
                                                document=dict(room))
