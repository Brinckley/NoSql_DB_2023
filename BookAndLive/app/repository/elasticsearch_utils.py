from elasticsearch import AsyncElasticsearch
import os

elasticsearch_client: AsyncElasticsearch = None


def get_es_client():
    return elasticsearch_client


async def connect_init_elasticsearch():
    global elasticsearch_client
    elasticsearch_uri = os.getenv('ELASTICSEARCH_URI')

    try:
        elasticsearch_client = AsyncElasticsearch(elasticsearch_uri)
        await elasticsearch_client.info()
        print(f'Connected to elasticsearch.py with uri {elasticsearch_uri}')
    except Exception as ex:
        print(f'Cant connect to Elasticsearch: {ex}')


async def close_elasticsearch_connect():
    global elasticsearch_client
    if elasticsearch_client is None:
        return
    await elasticsearch_client.close()