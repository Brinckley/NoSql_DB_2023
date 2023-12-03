from fastapi import APIRouter, HTTPException, Depends

from bson import ObjectId

from app.client.model import *

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
async def client_by_id(client_id: str):
    if not ObjectId.is_valid(client_id):
        raise HTTPException(status_code=400, detail='Bad Request')

    raise HTTPException(status_code=404, detail=f'Client with ID : {client_id} not found')


@client_router.post(
    "/",
    response_description="Created client ID",
    response_model=int
)
async def client_add(client_instance: ClientSchema):
    raise HTTPException(status_code=404, detail="Client already exists")


@client_router.put(
    "/{client_id}",
    response_description="Updated client",
    response_model=ClientSchema
)
async def client_update(client_id: str):
    if not ObjectId.is_valid(client_id):
        raise HTTPException(status_code=400, detail='Bad Request')
    raise HTTPException(status_code=404, detail=f'Client with ID : {client_id} not found')


@client_router.delete(
        "/{client_id}",
        response_description="Deleted client id",
        response_model=ClientSchema
)
async def delete_client(client_id: str):
    if not ObjectId.is_valid(client_id):
        raise HTTPException(status_code=400, detail='Bad Request')
    raise HTTPException(status_code=404, detail=f'Client with ID : {client_id} not found')
