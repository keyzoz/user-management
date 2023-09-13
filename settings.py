import os

from dotenv import load_dotenv

load_dotenv()

REAL_DATABASE_URL = os.getenv("REAL_DATABASE_URL")
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
REDIS_DB_URL = os.getenv("REDIS_DB_URL")

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRE_MINUTES = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

localstack_endpoint_url = os.getenv("localstack_endpoint_url")
