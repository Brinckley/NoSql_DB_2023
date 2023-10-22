from app.reservation.model import *


# in memory temporary storage
fake_reservations = []


# getting all reservations
def get_all_reservations():
    return fake_reservations


# getting reservation from mongoDb by ID
def get_reservation(reservation_id):
    return fake_reservations[reservation_id]


# adding another reservation to mongoDb
def add_reservation(reservation):
    fake_reservations.append(reservation)


# updating reservations data by id
def update_reservation(reservation_id, reservation):
    fake_reservations.append(reservation)


# deleting reservation by id
def delete_reservation(reservation_id):
    fake_reservations.remove(reservation_id)