import os
from motor.motor_asyncio import AsyncIOMotorClient
from elasticsearch import AsyncElasticsearch

db_client: AsyncIOMotorClient = None
elasticsearch_client: AsyncElasticsearch = None


def get_elasticsearch_client() -> AsyncElasticsearch:
    return elasticsearch_client


async def connect_and_init_db():
    global db_client
    mongo_uri = os.getenv('MONGO_URI')
    global elasticsearch_client
    elasticsearch_uri = os.getenv('ELASTICSEARCH_URI')
    try:
        db_client = AsyncIOMotorClient()
        await db_client.server_info()
        print(f'Connected to mongo with uri {mongo_uri}')
    except Exception as ex:
        print(f'Cant connect to mongo: {ex}')
    # try:
    #     elasticsearch_client = AsyncElasticsearch(elasticsearch_uri)
    #     await elasticsearch_client.info()
    #     print(f'Connected to elasticsearch with uri {elasticsearch_uri}')
    # except Exception as ex:
    #     print(f'Cant connect to elasticsearch: {ex}')


async def close_db_connect():
    global db_client
    if db_client is None:
        return 
    db_client.close()
    # global elasticsearch_client
    # if elasticsearch_client is None:
    #     return
    # await elasticsearch_client.close()
