from __future__ import annotations

import os
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from app.client.model import *
from app.reservation.model import *
from app.room.model import *

db_client: AsyncIOMotorClient = None


async def get_db_collection() -> AsyncIOMotorCollection:
    mongo_db = os.getenv('MONGO_DB')
    mongo_collection = os.getenv('MONGO_COLLECTION')

    return db_client.get_database(mongo_db).get_collection(mongo_collection)


async def connect_and_init_mongo():
    global db_client
    mongo_uri = os.getenv('MONGO_URI')
    mongo_db = os.getenv('MONGO_DB')
    mongo_collection = os.getenv('MONGO_COLLECTION')
    try:
        db_client = AsyncIOMotorClient(mongo_uri)
        await db_client.server_info()
        print(f'Connected to mongo with uri {mongo_uri}')
        if mongo_db not in await db_client.list_database_names():
            await db_client\
                .get_database(mongo_db)\
                .create_collection(mongo_collection)
            print(f'Database {mongo_db} created')

    except Exception as ex:
        print(f'Cant connect to mongo: {ex}')


async def close_db_connect():
    global db_client
    if db_client is None:
        return
    db_client.close()


def get_filter(id: str) -> dict:
    return {'id': ObjectId(id)}


def map_client(client: Any) -> ClientSchema | None:
    if client is None:
        return None
    return ClientSchema(id=str(client['id']), name=client['name'], email=client['email'])


def map_reservation(reservation: Any) -> ReservationSchema | None:
    if reservation is None:
        return None
    return ReservationSchema(id=str(reservation['id']), client_id=reservation['client_id'],
                             room_id=reservation['room_id'], booking_date=reservation['booking_gate'],
                             booking_status=reservation['booking_status'])
