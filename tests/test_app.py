from fastapi import status
from fastapi.testclient import TestClient
from main import app, get_settings


client = TestClient(app)



headers = {}
USER = {"username": "wera.watcharapon@gmail.com", "password": "kane!@#$"}

PAYLOAD_CARD = {
    "name": "name card",
    "content": "input your json",
    "description": "description card",
}


def get_token():
    token = client.post("/authentication/token", data=USER)
    token = token.json()["access_token"]
    headers["Authorization"] = "Bearer " + token


def test_card_create():
    get_token()
    response = client.post("/api/line/create", json=PAYLOAD_CARD, headers=headers)
    global ids_card
    ids_card = response.json()["_id"]
    assert response.status_code == status.HTTP_201_CREATED


def test_card_duplicate():
    response = client.post("/api/line/create", json=PAYLOAD_CARD, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "item name duplicate"}


def test_card_invalid():
    response = client.post(
        "/api/line/create", json=PAYLOAD_CARD.pop("name"), headers=headers
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]["msg"] == "value is not a valid dict"


def test_card_find():
    response = client.get(
        "/api/line/",
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) >= 1


def test_card_update():
    PAYLOAD_CARD["name"] = "update name card"
    response = client.put(
        f"/api/line/query/update/{ids_card}", json=PAYLOAD_CARD, headers=headers
    )
    assert response.status_code == status.HTTP_200_OK


def test_card_delete():
    response = client.delete(f"/api/line/query/delete/{ids_card}", headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_card_update_not_found():
    id = "fake_id_card"
    PAYLOAD_CARD["name"] = "update name card test unit"
    response = client.put(
        f"/api/line/query/update/{id}",
        json=PAYLOAD_CARD,
        headers=headers,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": f"Intent not found {id}"}


def test_card_delete_not_found():
    id = "fake_id_card"
    response = client.delete(f"/api/line/query/delete/{id}", headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": f"Card not found {id}"}


PAYLOAD_TEXT = {
    "access_token": "test unit access token",
    "user_id": "test line name",
    "message": "test send message",
}


def test_text():
    response = client.post("/api/line/text", json=PAYLOAD_TEXT, headers=headers)
    assert response.status_code == status.HTTP_200_OK


def test_text_not_found():
    PAYLOAD_TEXT["access_token"] = "fake access_token"
    response = client.post("/api/line/text", json=PAYLOAD_TEXT, headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        "detail": "Authentication failed. Confirm that the access token in the authorization header is valid."}


def test_text_user_id_not_found():
    PAYLOAD_TEXT["user_id"] = "fake user_id"
    response = client.post("/api/line/text", json=PAYLOAD_TEXT, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "The property, 'to', in the request body is invalid (line: -, column: -)"}


PAYLOAD_SEND_CARD = {
    "access_token": "test access token long live",
    "user_id": "test line name",
    "default_card": False,
    "id_card": "test id card",
}


def test_send_card():
    response = client.post("/api/line/card", json=PAYLOAD_SEND_CARD, headers=headers)
    ids_send_text = response.json()["_id"]
    assert response.status_code == status.HTTP_200_OK


def test_send_card_not_found():
    PAYLOAD_SEND_CARD["access_token"] = "fake access_token"
    response = client.post("/api/line/card", json=PAYLOAD_SEND_CARD, headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        "detail": "Authentication failed. Confirm that the access token in the authorization header is valid."}


def test_send_card_not_id_card():
    PAYLOAD_SEND_CARD["id_card"] = "fake id_card"
    response = client.post("/api/line/card", json=PAYLOAD_SEND_CARD, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "ID card not found"}


def test_send_card_not_user_id():
    PAYLOAD_SEND_CARD["user_id"] = "fake user_id"
    response = client.post("/api/line/card", json=PAYLOAD_SEND_CARD, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "The property, 'to', in the request body is invalid (line: -, column: -)"}


def test_send_card_default():
    PAYLOAD_SEND_CARD["default_card"] = True
    response = client.post("/api/line/card", json=PAYLOAD_SEND_CARD, headers=headers)
    assert response.status_code == status.HTTP_200_OK
