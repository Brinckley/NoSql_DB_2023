from fastapi import Depends

from motor.motor_asyncio import AsyncIOMotorCollection

from app.client.model import *
from app.repository.mongo_utils import get_mongo_client


class ClientMongoRepository:
    mongo_collection: AsyncIOMotorCollection

    @staticmethod
    def mongo_client_factory(mongo_collection: AsyncIOMotorCollection = Depends(get_mongo_client)):
        return ClientMongoRepository(mongo_collection)


    def get_client(self,
                   client_id: str) -> ClientSchema:
        # getting client data by id
        return ClientSchema()


    def add_client(self,
                   client: ClientSchema) -> str:
        return '0'


    def update_client(self,
                      client_id: str,
                      client: UpdateClientSchema) -> ClientSchema:
        return UpdateClientSchema()


    def delete_client(self,
                      client_id: str) -> ClientSchema:
        return ClientSchema()