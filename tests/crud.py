from sqlalchemy import insert

from src.db.models import Group, User
from tests.conftest import async_session_maker


async def create_only_user_data(user_data):
    async with async_session_maker() as session:
        user = insert(User).values(**user_data)
        await session.execute(user)
        await session.commit()


async def create_only_group_data(group_name):
    async with async_session_maker() as session:
        group = insert(Group).values(name=group_name)
        await session.execute(group)
        await session.commit()


async def create_user_and_group_data(user_data, group_name):
    await create_only_group_data(group_name=group_name)
    await create_only_user_data(user_data=user_data)
