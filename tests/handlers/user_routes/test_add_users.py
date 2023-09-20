import pytest
from sqlalchemy import insert

from src.db.models import Group, User
from tests.conftest import async_session_maker


async def test_add_groups():
    async with async_session_maker() as session:
        rows = ["Pandas", "Cows", "Rabbits"]
        role = insert(Group).values([{"name": name} for name in rows])
        await session.execute(role)
        await session.commit()


async def test_add_moderator():
    async with async_session_maker() as session:
        user = insert(User).values(
            user_id="c43df4fa-7131-40ad-9277-339de8303542",
            name="Dmitriy",
            surname="Slav",
            username="dslav",
            phone_number="+37431314534",
            email="dmslav@example.com",
            role="MODERATOR",
            image_s3="path/img2",
            group_name="Pandas",
            hashed_password="$2b$12$rnbnpPPhJBQhqeYwyZBUJu8DdF4ty7bTbAfd3O2jVEBmCyIV5Vkwy",
        )
        await session.execute(user)
        await session.commit()


async def test_add_admin():
    async with async_session_maker() as session:
        user = insert(User).values(
            user_id="a55ac1df-7331-40cd-0431-339de8304813",
            name="Alex",
            surname="Monarch",
            username="monarch",
            phone_number="+211941431",
            email="monarch@example.com",
            role="ADMIN",
            image_s3="path/img3",
            group_name="Pandas",
            hashed_password="$2b$12$rnbnpPPhJBQhqeYwyZBUJu8DdF4ty7bTbAfd3O2jVEBmCyIV5Vkwy",
        )
        await session.execute(user)
        await session.commit()
