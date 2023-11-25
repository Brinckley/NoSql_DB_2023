from mongo_utils import connect_and_init_db, close_db_connect
from elasticsearch_utils import connect_init_elasticsearch, close_elasticsearch_connect


async def startup_handling():
    await connect_and_init_db()
    await connect_init_elasticsearch()


async def shutdown_handling():
    await close_db_connect()
    await close_elasticsearch_connect()