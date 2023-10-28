import os
from motor.motor_asyncio import AsyncIOMotorClient

db_client: AsyncIOMotorClient = None

async def connect_and_init_db():
    global db_client
    mongo_uri = os.getenv('MONGO_URI')
    try:
        db_client = AsyncIOMotorClient()
        print('Connect to mongo')
    except Exception as ex:
        print(f'Cant connect to mongo: {ex}')

async def close_db_connect():
    global db_client
    if db_client is None:
        return 
    db_client.close()