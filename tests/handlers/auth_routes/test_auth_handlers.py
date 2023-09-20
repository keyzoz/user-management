import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import insert

from src.db.models import Group, User
from tests.conftest import async_session_maker


async def test_add_group():
    async with async_session_maker() as session:

        role = insert(Group).values(name="Lamas")
        await session.execute(role)
        await session.commit()


async def test_add_user():
    async with async_session_maker() as session:
        user = insert(User).values(
            user_id="e23df4fa-7331-40cd-9277-339de8303542",
            name="Victor",
            surname="Ivanov",
            username="vic",
            phone_number="+3741894314",
            email="vic@example.com",
            role="User",
            image_s3="path/img1",
            group_name="Lamas",
            hashed_password="$2b$12$rnbnpPPhJBQhqeYwyZBUJu8DdF4ty7bTbAfd3O2jVEBmCyIV5Vkwy",
        )
        await session.execute(user)
        await session.commit()


async def test_login_user(ac: AsyncClient):

    user_for_login = {
        "username": "vic",
        "password": "admin",
    }

    resp = await ac.post("/auth/token", data=user_for_login)

    data_from_resp = resp.json()

    assert "access_token" in data_from_resp
    assert "refresh_token" in data_from_resp
    assert data_from_resp["token_type"] == "Bearer"
