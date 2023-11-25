from fastapi import APIRouter, HTTPException, Depends
from app.reservation.model import *
from bson import ObjectId, Timestamp
from app.reservation.repository_mongo import *
from app.reservation.repository_elasticsearch import *


reservation_router = APIRouter(
    prefix="/reservations",
    tags=["reservations"],
    responses={404: {"description": "Not found"}},
)


@reservation_router.get(
    "/{reservation_id}",
    response_description="Single reservation with given ID",
    response_model=ReservationSchema
)
async def reservation_by_id(reservation_id: str,
                            mongo_repository: ReservationMongoRepository
                            = Depends(ReservationMongoRepository.mongo_reservation_factory)):
    if not ObjectId.is_valid(reservation_id):
        raise HTTPException(status_code=400, detail='Bad Request')

    if (reservation := await mongo_repository.get_reservation(reservation_id)) is not None:
        return {"reservation": reservation}
    raise HTTPException(status_code=404, detail=f'Reservation with ID : {reservation_id} not found')


@reservation_router.post(
    "/",
    response_description="Added reservation ID",
    response_model=str
)
async def reservation_add(reservation: ReservationSchema,
                          mongo_repository: ReservationMongoRepository = Depends(ReservationMongoRepository.mongo_reservation_factory),
                          es_repository: ReservationEsRepository = Depends(ReservationEsRepository.es_reservation_factory)):
    if (reservation_id := await mongo_repository.add_reservation(reservation)) is not None:
        await es_repository.create(reservation_id, reservation)
        return {"reservation_id": reservation_id}
    raise HTTPException(status_code=404, detail=f'Reservation with ID : {reservation_id} already exists')


@reservation_router.put(
    "/{reservation_id}",
    response_description="Updated reservation",
    response_model=UpdateReservationSchema
)
async def reservation_update(reservation_id: str,
                             reservation_upd: UpdateReservationSchema,
                             mongo_repository: ReservationMongoRepository = Depends(ReservationMongoRepository.mongo_reservation_factory),
                             es_repository: ReservationEsRepository = Depends(ReservationEsRepository.es_reservation_factory)):
    if not ObjectId.is_valid(reservation_id):
        raise HTTPException(status_code=400, detail='Bad Request')

    if (reservation := await mongo_repository.update_reservation(reservation_id, reservation_upd)) is not None:
        await es_repository.update(reservation_id, reservation_upd)
        return {"updated_reservation": reservation}
    raise HTTPException(status_code=404, detail=f'Reservation with ID : {reservation_id} not found')


@reservation_router.get(
    "/client/{client_id}",
    response_description="All reservations for given client",
    response_model=list[ReservationSchema]
)
async def reservations_by_client_id(client_id: str,
                                    es_repository: ReservationEsRepository = Depends(ReservationEsRepository.es_reservation_factory)):
    if not ObjectId.is_valid(client_id):
        raise HTTPException(status_code=400, detail='Bad Request')

    if (reservations := await es_repository.find_by_client_id(client_id)) is not None:
        return {"reservations": reservations}
    raise HTTPException(status_code=404, detail=f'No such client with ID: {client_id}')


@reservation_router.get(
    "/from/{time_from}/to/{time_to}",
    response_description="All reservations in the given period",
    response_model=list[ReservationSchema]
)
async def reservations_from_to(time_from: datetime,
                               time_to: datetime,
                               es_repository: ReservationEsRepository = Depends(ReservationEsRepository.es_reservation_factory)):
    if (reservations := await es_repository.find_by_range(time_from, time_to)) is not None:
        return {"reservations": reservations}
    raise HTTPException(status_code=404, detail=f'No reservations in this period: from {time_from}, to {time_to}')


@reservation_router.get(
    "/room/{room_id}",
    response_description="All reservations for this room",
    response_model=list[ReservationSchema]
)
async def reservations_by_room_id(room_id: str,
                                  es_repository: ReservationEsRepository = Depends(ReservationEsRepository.es_reservation_factory)):
    if not ObjectId.is_valid(room_id):
        raise HTTPException(status_code=400, detail='Bad Request')

    if (reservations := await es_repository.find_by_room_id(room_id)) is not None:
        return {"reservations": reservations}
    raise HTTPException(status_code=404, detail=f'No such room with ID: {room_id}')






























