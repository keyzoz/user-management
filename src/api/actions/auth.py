import os
import random
import string

import boto3
from fastapi.security import OAuth2PasswordBearer
from fastapi_jwt_auth import AuthJWT
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from settings import localstack_endpoint_url
from src.api.schemas import Settings
from src.db.dals import UserDAL
from src.db.models import User
from src.hashing import Hasher

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


async def _get_user_by_username_for_auth(username: str, session: AsyncSession):
    async with session.begin():
        user_dal = UserDAL(session)
        return await user_dal.get_user_by_username(
            username=username,
        )


async def authenticate_user(
    username: str, password: str, session: AsyncSession
) -> User | None:
    user = await _get_user_by_username_for_auth(username=username, session=session)
    if user is None:
        return
    if not Hasher.verify_password(password, user.hashed_password):
        return
    return user


def generate_reset_password_token(length: int = 32):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


async def send_reset_token(email: str, reset_token):
    ses_client = boto3.client(
        "ses",
        region_name="us-east-1",
        endpoint_url=localstack_endpoint_url,
    )

    subject = "Reset Password"
    body = f"Password reset link: http://localhost:8000/auth/reset-password?token={reset_token}"

    response = ses_client.send_email(
        Source="sender@example.com",
        Destination={"ToAddresses": [email]},
        Message={"Subject": {"Data": subject}, "Body": {"Text": {"Data": body}}},
    )
    return response


@AuthJWT.load_config
def get_config():
    return Settings()
