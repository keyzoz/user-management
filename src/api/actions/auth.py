from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi_jwt_auth import AuthJWT
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

import settings
from src.api.schemas import Settings
from src.db.dals import UserDAL
from src.db.database import get_db
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


@AuthJWT.load_config
def get_config():
    return Settings()
