import os

from motor.motor_asyncio import AsyncIOMotorClient

db_client: AsyncIOMotorClient = None


def get_mongo_client():
    return db_client


async def connect_and_init_db():
    global db_client
    mongo_uri = os.getenv('MONGO_URI')
    try:
        db_client = AsyncIOMotorClient()
        await db_client.server_info()
        print(f'Connected to mongo with uri {mongo_uri}')
    except Exception as ex:
        print(f'Cant connect to mongo: {ex}')


async def close_db_connect():
    global db_client
    if db_client is None:
        return 
    db_client.close()
