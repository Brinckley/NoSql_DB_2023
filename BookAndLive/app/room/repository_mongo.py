from app.room.model import *

# in memory temporary storage
fake_rooms = []


# getting all rooms for start page (list all rooms)
def get_all_rooms():
    return fake_rooms


# getting room from mongoDb by ID
def get_room(room_id):
    return fake_rooms[room_id]


# adding another room to mongoDb
def add_room(room):
    fake_rooms.append(room)


# updating rooms data by id
def update_room(room_id, room):
    fake_rooms.append(room)


# deleting room by id
def delete_room(room_id):
    fake_rooms.remove(room_id)