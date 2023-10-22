from fastapi import APIRouter, HTTPException
from app.client.model import *
from app.client.repository_mongo import *

client_router = APIRouter(
    prefix="/client",
    tags=["client"],
    responses={404: {"description": "Not found"}},
)


# Client profile. Displaying data.
@client_router.get(
    "/{client_id}",
    response_description="Get client profile",
    response_model=ClientSchema
)
async def client_by_id(client_id: str):
    if (client := await get_client(client_id)) is not None:
        return client
    raise HTTPException(status_code=404, detail=f'Client with ID : {client_id} not found')


# Create another client
@client_router.post(
    "/",
    response_description="Create client"
)
async def client_add(client: ClientSchema):
    if (client := await get_client(client.id)) is not None:
        add_client(client)


# Update the client data
@client_router.put(
    "/{client_id}",
    response_description="Update client profile",
    response_model=ClientSchema
)
async def client_update(client_id: str, client: ClientSchema):
    if (client := await get_client(client_id)) is not None:
        update_client(client_id, client)