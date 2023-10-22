from app.client.model import *


# in memory temporary storage
fake_clients = []


# getting client info by id
def get_client(client_id):
    # getting client data by id
    return fake_clients[client_id]


# adding new client to the db
def add_client(client):
    fake_clients.append(client)


# updating clients data by id
def update_client(client_id, client):
    fake_clients.append(client)