import os
from fastapi import Depends
from datetime import datetime

from elasticsearch import AsyncElasticsearch

from app.repository.elasticsearch_utils import get_elasticsearch_client
from app.reservation.model import ReservationSchema, UpdateReservationSchema


class ReservationEsRepository:
    _elasticsearch_client: AsyncElasticsearch
    _elasticsearch_index: str

    def __init__(self, index: str, elasticsearch_client: AsyncElasticsearch):
        self._elasticsearch_client = elasticsearch_client
        self._elasticsearch_index = index

    @staticmethod
    def es_reservation_factory(elasticsearch_client: AsyncElasticsearch = Depends(get_elasticsearch_client)):
        elasticsearch_index = os.getenv('ELASTICSEARCH_INDEX_RESERVATION')
        return ReservationEsRepository(elasticsearch_index, elasticsearch_client)

    async def create(self, reservation_id: str, reservation: ReservationSchema):
        await self._elasticsearch_client.create(index=self._elasticsearch_index, id=reservation_id,
                                                document=dict(reservation))

    async def update(self, reservation_id: str, reservation: UpdateReservationSchema):
        await self._elasticsearch_client.update(index=self._elasticsearch_index, id=reservation_id,
                                                doc=dict(reservation))

    async def delete(self, reservation_id: str):
        await self._elasticsearch_client.delete(index=self._elasticsearch_index, id=reservation_id)

    async def find_by_client_id(self, client_id: str) -> list:
        name_query = {
            "query": {
                "match": {
                    "client_id": client_id
                }
            }
        }
        reservations = await self.find_by_query(name_query)
        return reservations

    async def find_by_booking_date(self, booking_date: datetime) -> list:
        booking_date_query = {
            "query": {
                "match": {
                    "booking_date": booking_date
                }
            }
        }
        reservations = await self.find_by_query(booking_date_query)
        return reservations

    async def find_by_range(self, left_date: datetime, right_date: datetime) -> list:
        range_date_query = {
            "query": {
                "range": {
                    "datetime": {
                        "gte": left_date,
                        "lte": right_date,
                    }
                }
            }
        }
        reservations = await self.find_by_query(range_date_query)
        return reservations

    async def find_by_room_id(self, room_id: str) -> list:
        booking_date_query = {
            "query": {
                "match": {
                    "_id": room_id
                }
            }
        }
        reservations = await self.find_by_query(booking_date_query)
        return reservations

    async def find_by_query(self, query) -> list:
        response = await self._elasticsearch_client.search(index=self._elasticsearch_index, query=query,
                                                           filter_path=['hits.hits._id', 'hits.hits._source'])
        if 'hits' not in response.body:
            return []
        result = response.body['hits']['hits']
        reservations = list(map(lambda reservation:
                                ReservationSchema(id=reservation['_id'],
                                                  client_id=reservation['_source']['client_id'],
                                                  room_id=reservation['_source']['room_id'],
                                                  booking_date=reservation['_source']['booking_date'],
                                                  booking_status=reservation['_source']['booking_status']), result))
        return reservations