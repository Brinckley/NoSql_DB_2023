import requests

BASE_ENDPOINT_CLIENTS = "http://localhost:8000/clients"


def test_can_call_endpoint_clients():
    response = requests.get(BASE_ENDPOINT_CLIENTS)
    assert response.status_code == 200


def test_get_client():
    payload_post_client = {
        "name": "test_client",
        "email": "test_client@gmail.com"
    }
    response_post = requests.post(BASE_ENDPOINT_CLIENTS + "/", json=payload_post_client)
    assert response_post.status_code == 200
    response_put_data = response_post.json()
    client_id = response_put_data["client_id"]

    response_get = requests.get(BASE_ENDPOINT_CLIENTS + f"/{client_id}/")
    assert response_get.status_code == 200
    response_get_data = response_get.json()
    assert response_get_data["id"] == client_id
    assert response_get_data["name"] == payload_post_client["name"]
    assert response_get_data["email"] == payload_post_client["email"]


def test_put_client():
    payload_post_client = {
        "name": "test_client_another",
        "email": "test_client_another@gmail.com"
    }
    response_post = requests.post(BASE_ENDPOINT_CLIENTS + "/", json=payload_post_client)
    assert response_post.status_code == 200
    response_put_data = response_post.json()
    client_id = response_put_data["client_id"]

    payload_put_client = {
        "name": "test_client_another_put",
        "email": "test_client_another_put@gmail.com"
    }
    response_put = requests.put(BASE_ENDPOINT_CLIENTS + f"/{client_id}/", json=payload_put_client)
    assert response_put.status_code == 200
    response_put_data = response_put.json()
    assert response_put_data["id"] == client_id
    assert response_put_data["name"] == payload_put_client["name"]
    assert response_put_data["email"] == payload_put_client["email"]

    response_get = requests.get(BASE_ENDPOINT_CLIENTS + f"/{client_id}/")
    assert response_get.status_code == 200
    response_get_data = response_get.json()
    assert response_get_data["id"] == client_id
    assert response_get_data["name"] == payload_put_client["name"]
    assert response_get_data["email"] == payload_put_client["email"]


def test_delete_client():
    payload_post_client = {
        "name": "test_client_delete",
        "email": "test_client_delete@gmail.com"
    }
    response_post = requests.post(BASE_ENDPOINT_CLIENTS + "/", json=payload_post_client)
    assert response_post.status_code == 200
    response_post_data = response_post.json()
    client_id = response_post_data["client_id"]

    response_delete = requests.delete(BASE_ENDPOINT_CLIENTS + f"/{client_id}/")
    assert response_delete.status_code == 200
    response_put_data = response_delete.json()
    assert response_put_data["client_id"] == client_id
