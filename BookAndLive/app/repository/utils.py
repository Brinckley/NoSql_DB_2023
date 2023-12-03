from app.repository.mongo_utils import connect_and_init_db, close_db_connect
from app.repository.elasticsearch_utils import connect_init_elasticsearch, close_elasticsearch_connect


async def startup_handling():
    print('START------------------------------')
    await connect_and_init_db()
    await connect_init_elasticsearch()


async def shutdown_handling():
    print('CLOSE')
    await close_db_connect()
    await close_elasticsearch_connect()