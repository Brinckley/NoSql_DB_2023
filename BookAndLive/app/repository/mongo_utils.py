from __future__ import annotations

import os
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from app.client.model import *
from app.reservation.model import *


db_client: AsyncIOMotorClient = None


async def get_mongo_client() -> AsyncIOMotorCollection:
    mongo_db = os.getenv('MONGO_DB')
    mongo_collection_client = os.getenv('MONGO_COLLECTION_CLIENT')
    return db_client.get_database(mongo_db).get_collection(mongo_collection_client)


async def get_mongo_reservation() -> AsyncIOMotorCollection:
    mongo_db = os.getenv('MONGO_DB')
    mongo_collection_reservation = os.getenv('MONGO_COLLECTION_RESERVATION')
    return db_client.get_database(mongo_db).get_collection(mongo_collection_reservation)


async def connect_and_init_db():
    print('UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU')
    global db_client
    mongo_uri = os.getenv('MONGO_URI')
    print(f"URI : {mongo_uri}")
    mongo_db = os.getenv('MONGO_DB')
    mongo_collection_client = os.getenv('MONGO_COLLECTION_CLIENT')
    mongo_collection_reservation = os.getenv('MONGO_COLLECTION_RESERVATION')
    try:
        db_client = AsyncIOMotorClient(mongo_uri)
        await db_client.server_info()
        print(f'Connected to mongo with uri {mongo_uri}')
        if mongo_db not in await db_client.list_database_names():
            await db_client\
                .get_database(mongo_db)\
                .create_collection(mongo_collection_client)
            await db_client\
                .get_database(mongo_db)\
                .create_collection(mongo_collection_reservation)
            print(f'Database {mongo_db} created')
    except Exception as ex:
        print(f'Cant connect to mongo: {ex}')


async def close_db_connect():
    global db_client
    if db_client is None:
        return 
    db_client.close()


def get_filter(id: str) -> dict:
    return {'_id': ObjectId(id)}


def map_client(client: Any) -> ClientSchema | None:
    if client is None:
        return None
    return ClientSchema(id=str(client['_id']), name=client['name'], email=client['email'])


def map_reservation(reservation: Any) -> ReservationSchema | None:
    if reservation is None:
        return None
    return ReservationSchema(id=str(reservation['_id']), client_id=reservation['client_id'], room_id=reservation['room_id'], booking_date=reservation['booking_gate'], booking_status=reservation['booking_status'])