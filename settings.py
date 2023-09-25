import os

from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

POSTGRES_TEST_USER = os.getenv("POSTGRES_TEST_USER")
POSTGRES_TEST_PASSWORD = os.getenv("POSTGRES_TEST_PASSWORD")
POSTGRES_TEST_DB = os.getenv("POSTGRES_TEST_DB")
POSTGRES_TEST_HOST = os.getenv("POSTGRES_TEST_HOST")
POSTGRES_TEST_PORT = os.getenv("POSTGRES_TEST_PORT")


REAL_DATABASE_URL = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/"
    f"{POSTGRES_DB}"
)
TEST_DATABASE_URL = (
    f"postgresql+asyncpg://{POSTGRES_TEST_USER}:{POSTGRES_TEST_PASSWORD}@{POSTGRES_TEST_HOST}:{POSTGRES_TEST_PORT}/"
    f"{POSTGRES_TEST_DB}"
)

REDIS_DB_URL = os.getenv("REDIS_DB_URL")

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRE_MINUTES = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

AWS_EMAIL_SENDER = os.getenv("AWS_EMAIL_SENDER")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

localstack_endpoint_url = os.getenv("localstack_endpoint_url")
