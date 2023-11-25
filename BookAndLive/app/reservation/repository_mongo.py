from fastapi import Depends

from motor.motor_asyncio import AsyncIOMotorCollection

from app.repository.mongo_utils import get_mongo_client
from app.reservation.model import *


class ReservationMongoRepository:
    mongo_collection: AsyncIOMotorCollection

    @staticmethod
    def mongo_reservation_factory(mongo_collection: AsyncIOMotorCollection = Depends(get_mongo_client)):
        return ReservationMongoRepository(mongo_collection)

    def get_all_reservations_by_client_id(self,
                                          client_id: str) -> list:
        return [ReservationSchema()]

    def get_reservation(self,
                        reservation_id: str) -> ReservationSchema:
        return ReservationSchema()

    def add_reservation(self,
                        reservation: ReservationSchema) -> str:
        return ""

    def update_reservation(self,
                           reservation_id: str,
                           reservation: UpdateReservationSchema) -> ReservationSchema:
        return ReservationSchema()

    def delete_reservation(self,
                           reservation_id: str) -> ReservationSchema:
        return ReservationSchema()