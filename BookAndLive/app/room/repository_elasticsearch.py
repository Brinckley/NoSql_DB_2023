import os
from fastapi import Depends
from datetime import datetime

from elasticsearch import AsyncElasticsearch

from app.repository.elasticsearch_utils import get_elasticsearch_client
from app.room.model import RoomSchema, UpdateRoomSchema


class RoomEsRepository:
    _elasticsearch_client: AsyncElasticsearch
    _elasticsearch_index: str

    def __init__(self, index: str, elasticsearch_client: AsyncElasticsearch):
        self._elasticsearch_client = elasticsearch_client
        self._elasticsearch_index = index

    @staticmethod
    def es_client_factory(elasticsearch_client: AsyncElasticsearch = Depends(get_elasticsearch_client)):
        elasticsearch_index = os.getenv('ELASTICSEARCH_INDEX_ROOM')
        return RoomEsRepository(elasticsearch_index, elasticsearch_client)

    async def create(self, room_id: str, room: UpdateRoomSchema):
        await self._elasticsearch_client.create(index=self._elasticsearch_index, id=room_id,
                                                document=dict(room))

    async def update(self, room_id: str, room: UpdateRoomSchema):
        await self._elasticsearch_client.update(index=self._elasticsearch_index, id=room_id,
                                                doc=dict(room))

    async def delete(self, room_id: str):
        await self._elasticsearch_client.delete(index=self._elasticsearch_index, id=room_id)

    async def find_by_attributes(self, attributes: str):
        attributes = attributes.replace('+', ' ')
        attributes_query = {
            "query": {
                "query_string": {
                    "query": attributes,
                    "default_field": "attributes",
                },
                'match': {
                    "booking_status": True
                }
            }
        }
        rooms = await self.find_by_query(attributes_query)
        return rooms

    async def find_by_country(self, country_name: str):
        country_name_query = {
            "query": {
                "bool": {
                    "filter": {
                        {"booking_status": True},
                        {"address.country": country_name},
                    }
                }
            }
        }
        rooms = await self.find_by_query(country_name_query)
        return rooms

    async def find_by_city(self, city_name: str):
        city_name_query = {
            "query": {
                "bool": {
                    "filter": {
                        {"booking_status": True},
                        {"address.city": city_name},
                    }
                }
            }
        }
        rooms = await self.find_by_query(city_name_query)
        return rooms

    async def find_available(self):
        availability_query = {
            "query": {
                "match": {
                    "booking_status": True
                }
            }
        }
        rooms = await self.find_by_query(availability_query)
        return rooms

    async def find_by_query(self, filter_query) -> list:
        response = await self._elasticsearch_client.search(index=self._elasticsearch_index, query=filter_query,
                                                           filter_path=['hits.hits._id', 'hits.hits._source'])
        if 'hits' not in response.body:
            return []
        result = response.body['hits']['hits']
        rooms = list(map(lambda room:
                         RoomSchema(id=room['id'],
                                    description=room['_source'][''],
                                    attributes=room['_source'][''],
                                    booking_status=room['_source'][''],
                                    country=room['_source']['address']['country'],
                                    city=room['_source']['address']['city'],
                                    address=room['_source']['address']['address']), result))
        return rooms
