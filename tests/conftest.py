import asyncio
import random
from typing import AsyncGenerator

import aioboto3
import boto3
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

engine_test = create_async_engine(settings.TEST_DATABASE_URL, future=True, echo=True)
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

    group_data = fake.word()

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
        "role": "USER",
        "email": fake.email(),
        "image_s3": fake.url(),
        "hashed_password": Hasher.get_password_hash(password),
    }

    return password, user_data


@pytest.fixture(scope="function")
def generate_random_moderator_data():

    password = fake.password()
    user_data = {
        "user_id": str(fake.uuid4()),
        "name": fake.first_name(),
        "surname": fake.last_name(),
        "username": fake.user_name(),
        "phone_number": fake.phone_number(),
        "role": "MODERATOR",
        "email": fake.email(),
        "image_s3": fake.url(),
        "hashed_password": Hasher.get_password_hash(password),
    }

    return password, user_data


@pytest.fixture(scope="function")
def generate_random_admin_data():

    password = fake.password()
    user_data = {
        "user_id": str(fake.uuid4()),
        "name": fake.first_name(),
        "surname": fake.last_name(),
        "username": fake.user_name(),
        "phone_number": fake.phone_number(),
        "role": "ADMIN",
        "email": fake.email(),
        "image_s3": fake.url(),
        "hashed_password": Hasher.get_password_hash(password),
    }

    return password, user_data


@pytest.fixture(autouse=True, scope="session")
async def s3():
    aws_session = aioboto3.Session()
    async with aws_session.client(
        "s3",
        region_name=settings.AWS_REGION,
        endpoint_url=settings.LOCALSTACK_ENDPOINT_URL,
    ) as s3:
        await s3.create_bucket(Bucket=settings.SES_BUCKET_NAME)


@pytest.fixture(autouse=True, scope="session")
async def ses():
    ses_client = boto3.client(
        "ses",
        region_name=settings.AWS_REGION,
        endpoint_url=settings.LOCALSTACK_ENDPOINT_URL,
    )
    ses_client.verify_email_identity(EmailAddress=settings.AWS_EMAIL_SENDER)
