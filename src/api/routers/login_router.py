from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

import settings
from src.api.actions.auth import authenticate_user
from src.api.schemas import Token
from src.db.database import get_db


login_router = APIRouter()


@login_router.post('/token', response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
          Authorize: AuthJWT = Depends(), session: AsyncSession = Depends(get_db),):
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = Authorize.create_access_token(subject=user.username)
    refresh_token = Authorize.create_refresh_token(subject=user.username)
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="Bearer")