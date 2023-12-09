from fastapi import APIRouter, HTTPException

from app.repository.memcached_utils import *

from app.client.repository_mongo import *
from app.client.repository_elasticsearch import *
from app.repository.memcached_utils import *

client_router = APIRouter(
    prefix="/client",
    tags=["client"],
    responses={404: {"description": "Not found"}},
)


@client_router.get(
    "/{client_id}",
    response_description="Found client profile",
    response_model=ClientSchema
)
async def client_by_id(client_id: str,  # need to think about type
                       mongo_repository: ClientMongoRepository = Depends(ClientMongoRepository.mongo_client_factory)):
                       #memcached_client: HashClient = Depends(get_memcached_client)
    if not ObjectId.is_valid(client_id):
        raise HTTPException(status_code=400, detail='Bad Request')
    # print("dsf")
    # client = memcached_client.get(client_id)
    # if client is not None:
    #     return {"client": client}
    if (client := await mongo_repository.get_client(str(client_id))) is not None:
        return {"client": client}
    # memcached_client.add(client_id, client)

    raise HTTPException(status_code=404, detail=f'Client with ID : {client_id} not found')


@client_router.post("/")
async def client_add(client_instance: UpdateClientSchema,
                     es_repository: ClientEsRepository = Depends(ClientEsRepository.es_client_factory),
                     mongo_repository: ClientMongoRepository = Depends(ClientMongoRepository.mongo_client_factory)):
    if (client_id := await mongo_repository.add_client(client_instance)) is not None:
        await es_repository.create(client_id, client_instance)
        return client_id
    raise HTTPException(status_code=404, detail="Client already exists")


@client_router.put(
    "/{client_id}",
    response_description="Updated client",
    response_model=ClientSchema
)
async def client_update(client_id: str,
                        client_upd: UpdateClientSchema,
                        es_repository: ClientEsRepository = Depends(ClientEsRepository.es_client_factory),
                        mongo_repository: ClientMongoRepository = Depends(ClientMongoRepository.mongo_client_factory)):
    if not ObjectId.is_valid(client_id):
        raise HTTPException(status_code=400, detail='Bad Request')

    if (updated_client := await mongo_repository.update_client(str(client_id), client_upd)) is not None:
        await es_repository.update(str(client_id), client_upd)
        return {"updated_client": updated_client}
    raise HTTPException(status_code=404, detail=f'Client with ID : {client_id} not found')


@client_router.delete(
    "/{client_id}",
    response_description="Deleted client id",
    response_model=ClientSchema
)
async def delete_client(client_id: str,
                        es_repository: ClientEsRepository = Depends(ClientEsRepository.es_client_factory),
                        mongo_repository: ClientMongoRepository = Depends(ClientMongoRepository.mongo_client_factory)):
    if not ObjectId.is_valid(client_id):
        raise HTTPException(status_code=400, detail='Bad Request')

    if (deleted_client := await mongo_repository.delete_client(str(client_id))) is not None:
        await es_repository.delete(str(client_id))
        return {"client_id": deleted_client}
    raise HTTPException(status_code=404, detail=f'Client with ID : {client_id} not found')
