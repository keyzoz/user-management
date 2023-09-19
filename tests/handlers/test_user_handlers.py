from httpx import AsyncClient
from sqlalchemy import insert, select

from src.db.models import Group
from tests.conftest import async_session_maker


async def test_add_group():
    async with async_session_maker() as session:
        role = insert(Group).values(name="Pandas")
        await session.execute(role)
        await session.commit()


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
    assert resp.status_code == 200
    assert data_from_resp["name"] == user_data["name"]
    assert data_from_resp["surname"] == user_data["surname"]
    assert data_from_resp["username"] == user_data["username"]
    assert data_from_resp["phone_number"] == user_data["phone_number"]
    assert data_from_resp["image_s3"] == user_data["image_s3"]
    assert data_from_resp["group_name"] == user_data["group_name"]


async def test_login_user(ac: AsyncClient):

    user_for_login = {
        "username": "alexlost21",
        "password": "string",
    }

    resp = await ac.post("/auth/token", data=user_for_login)

    data_from_resp = resp.json()

    assert "access_token" in data_from_resp
    assert "refresh_token" in data_from_resp
    assert data_from_resp["token_type"] == "Bearer"
