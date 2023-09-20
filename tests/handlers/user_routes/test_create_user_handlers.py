from fastapi import status
from httpx import AsyncClient


async def test_create_user(ac: AsyncClient):
    user_data = {
        "name": "Alex",
        "surname": "Lost",
        "username": "alexlost21",
        "phone_number": "+79525024142",
        "email": "alex21@example.com",
        "image_s3": "string",
        "password": "string",
        "group_name": "Pandas",
    }

    resp = await ac.post("/user/signup", json=user_data)

    data_from_resp = resp.json()
    assert resp.status_code == status.HTTP_200_OK
    assert data_from_resp["name"] == user_data["name"]
    assert data_from_resp["surname"] == user_data["surname"]
    assert data_from_resp["username"] == user_data["username"]
    assert data_from_resp["phone_number"] == user_data["phone_number"]
    assert data_from_resp["image_s3"] == user_data["image_s3"]
    assert data_from_resp["group_name"] == user_data["group_name"]
