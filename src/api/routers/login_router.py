from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.api.actions.auth import authenticate_user
from src.api.actions.token import (generate_reset_password_token,
                                   get_reset_token, send_reset_token,
                                   store_reset_token, get_jti, store_jti)
from src.api.actions.user import UserCRUD
from src.api.schemas import Token
from src.db.database import get_db
from src.db.redis_db import get_redis_client

login_router = APIRouter()

email_token = {}


@login_router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    Authorize: AuthJWT = Depends(),
    session: AsyncSession = Depends(get_db),
):
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = Authorize.create_access_token(subject=user.username)
    refresh_token = Authorize.create_refresh_token(subject=user.username)
    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="Bearer"
    )


@login_router.post("/refresh-token")
def refresh(Authorize: AuthJWT = Depends(), redis=Depends(get_redis_client)):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception:
        raise HTTPException(
            status_code=498,
            detail="Invalid Token/ Refresh Token Required",
        )
    current_user = Authorize.get_jwt_subject()
    jti_of_token = Authorize.get_raw_jwt().get('jti')
    try:
        store_token = get_jti(redis, username=current_user)
    except Exception as e:
        return {"error": f"error: {str(e)}"}
    print(store_token)
    if store_token.decode('utf-8') == jti_of_token:
        raise HTTPException(
            status_code=422,
            detail="Old Token",
        )

    store_jti(redis, current_user, jti_of_token)
    new_access_token = Authorize.create_access_token(subject=current_user)
    new_refresh_token = Authorize.create_refresh_token(subject=current_user)
    return Token(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="Bearer",
    )


@login_router.post("/sent-reset-link")
async def sent_reset_link(
    email: str, session: AsyncSession = Depends(get_db), redis=Depends(get_redis_client)
):
    user = await UserCRUD.get_user_by_email(email, session)
    if user:
        try:
            reset_token = generate_reset_password_token()
            store_reset_token(redis, email, reset_token)
            send_reset_token(email, reset_token)

            return {"message": "The token has been sent"}
        except Exception as e:
            return {"error": f"Error: {str(e)}"}

    else:
        raise HTTPException(
            status_code=404,
            detail="Email has not found",
        )


@login_router.post("/reset-password")
async def reset_password(
    email: str,
    token: str,
    new_password: str,
    confirm_password: str,
    session: AsyncSession = Depends(get_db),
    redis=Depends(get_redis_client),
):
    try:
        store_token = get_reset_token(redis, email)
        if store_token == token and new_password == confirm_password:
            updated_user = await UserCRUD.change_user_password(
                email, new_password, session
            )

            if updated_user:
                redis.delete(email)
                return {"message": "password has been changed"}
            else:
                return {"message": "error change"}
        else:
            return {"message": "error"}
    except Exception as e:
        return {"error": f"error {str(e)}"}
