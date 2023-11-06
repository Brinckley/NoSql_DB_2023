import os
from fastapi import Depends
from datetime import datetime

from elasticsearch import AsyncElasticsearch

from app.repository.elasticsearch_utils import get_es_client
from app.reservation.model import ReservationSchema, UpdateReservationSchema


class ReservationSearchRepository:
    _elasticsearch_client: AsyncElasticsearch
    _elasticsearch_index: str

    def __int__(self, elasticsearch_client: AsyncElasticsearch, index: str):
        self._elasticsearch_client = elasticsearch_client
        self._elasticsearch_index = index

    async def create(self, reservation_id: str, reservation: ReservationSchema):
        await self._elasticsearch_client.create(index=self._elasticsearch_index, id=reservation_id,
                                                document=dict(reservation))

    async def update(self, reservation_id: str, reservation: UpdateReservationSchema):
        await self._elasticsearch_client.update(index=self._elasticsearch_index, id=reservation_id,
                                                doc=dict(reservation))

    async def delete(self, reservation_id: str):
        await self._elasticsearch_client.delete(index=self._elasticsearch_index, id=reservation_id)

    async def find_by_booking_date(self, booking_date: datetime):  # logic not written yet
        return

    async def find_by_range(self, left: datetime, right: datetime):  # logic not written yet
        return

    async def find_by_room_id(self, _id: str):  # logic not written yet
        return

    @staticmethod
    def es_client_factory(elasticsearch_client: AsyncElasticsearch = Depends(get_es_client)):
        elasticsearch_index = os.getenv('ELASTICSEARCH_INDEX')
        return ReservationSearchRepository(elasticsearch_client, elasticsearch_index)