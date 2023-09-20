import asyncio
import random
from typing import AsyncGenerator
from unittest.mock import AsyncMock, patch

import pytest
from faker import Faker
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

import settings
from main import app
from src.db.database import get_db
from src.db.models import base
from src.hashing import Hasher

fake = Faker()

engine_test = create_async_engine(settings.TEST_DATABASE_URL, pool_pre_ping=True)
async_session_maker = sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)
base.metadata.bind = engine_test


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_db] = override_get_async_session


@pytest.fixture(autouse=True, scope="session")
async def prepare_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(base.metadata.drop_all)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function")
def generate_group_name():

    group_data = {"group_name": fake.word()}

    return group_data


@pytest.fixture(scope="function")
def generate_data_for_signup():

    user_data = {
        "name": fake.first_name(),
        "surname": fake.last_name(),
        "username": fake.user_name(),
        "phone_number": str(random.randint(0, 100000000)),
        "email": fake.email(),
        "image_s3": fake.url(),
        "password": fake.password(),
    }

    return user_data


@pytest.fixture(scope="function")
def generate_random_user_data():

    password = fake.password()
    user_data = {
        "user_id": str(fake.uuid4()),
        "name": fake.first_name(),
        "surname": fake.last_name(),
        "username": fake.user_name(),
        "phone_number": fake.phone_number(),
        "email": fake.email(),
        "image_s3": fake.url(),
        "hashed_password": Hasher.get_password_hash(password),
    }

    return password, user_data
