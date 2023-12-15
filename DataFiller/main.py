import csv
import random
import asyncio

from repository.utils.utils import *

from repository.elastic_repo import *
from repository.mongo_repo import *

LENGTH = 100


def letters(name):
    return ''.join(filter(str.isalpha, name))


async def fill_clients():
    clients = []
    with open("dumpData/Users.csv", encoding='utf-8') as r_file:
        file_reader = csv.DictReader(r_file, delimiter=",")
        count = 0
        for row in file_reader:
            if count == 0:
                print(f'{", ".join(row)}')
            client = UpdateClientSchema(name=str(row["DisplayName"]),
                                        email=str(letters(row["DisplayName"]) + str(row["Id"]) + "@gmail.com"))
            print(f"{count}: {client}")
            clients.append(client)
            count += 1
            if count == LENGTH:
                break
    return clients


async def fill_rooms():
    rooms = []
    with open("dumpData/Rooms_auckland_dump.csv", encoding='utf-8') as r_file:
        file_reader = csv.DictReader(r_file, delimiter=",")
        count = 0
        for row in file_reader:
            if count == 0:
                print(f'{", ".join(row)}')
            room = UpdateRoomSchema(
                description=str("Overall Satisfaction " + str(row["overall_satisfaction"])),
                attributes=str(row["room_type"]),
                booking_status=count % 3 == 0,
                full_address=Address(country="NewZealand", city="Auckland", address=str(row["neighborhood"])))
            print(f"{count}: {room}")
            rooms.append(room)
            count += 1
            if count == LENGTH:
                break
    return rooms


async def fill_reservations():
    await startup_handling()

    es_cl = get_elasticsearch_client()
    es_cl_repo = ClientEsRepository(es_cl)
    es_res_repo = ReservationEsRepository(es_cl)
    es_room_repo = RoomEsRepository(es_cl)

    mg_cl_repo = ClientMongoRepository(await get_mongo_client())
    mg_res_repo = ReservationMongoRepository(await get_mongo_reservation())
    mg_room_repo = RoomMongoRepository(await get_mongo_room())

    clients = await fill_clients()
    rooms = await fill_rooms()

    for i in range(LENGTH):
        random.seed(i + LENGTH + 456)
        print(i)
        client = clients[i]
        if (client_id := await mg_cl_repo.add_client(client)) is not None:
            await es_cl_repo.create(client_id, client)
        print(f"{client_id} : {client}")

        room = rooms[i]
        if (room_id := await mg_room_repo.add_room(room)) is not None:
            await es_room_repo.create(room_id, room)
        print(f"{room_id} : {room}")

        reservation = UpdateReservationSchema(
            room_id=str(room_id),
            client_id=str(client_id),
            booking_status=BookStatusEnum.paid,
            booking_date=f"2022-{random.randint(10,12)}-{random.randint(10,28)}T00:00:00")
        if (reservation_id := await mg_res_repo.add_reservation(reservation)) is not None:
            await es_res_repo.create(reservation_id, reservation)
        print(f"{reservation_id} : {reservation}")
        print("------------------------------------------------------------------------------")

    await shutdown_handling()

asyncio.run(fill_reservations())
