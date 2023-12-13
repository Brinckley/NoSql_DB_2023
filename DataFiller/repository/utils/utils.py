import asyncio

from repository.utils.elasticsearch_utils import connect_and_init_elasticsearch, close_elasticsearch_connect
from repository.utils.mongo_utils import connect_and_init_mongo, close_db_connect


async def startup_handling():
    print('----------START----------')
    await asyncio.gather(connect_and_init_mongo(), connect_and_init_elasticsearch())


async def shutdown_handling():
    print('----------CLOSE----------')
    await close_db_connect()
    await close_elasticsearch_connect()
