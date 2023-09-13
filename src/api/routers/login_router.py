from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.api.actions.auth import (authenticate_user,
                                  generate_reset_password_token,
                                  send_reset_token)
from src.api.actions.user import UserCRUD
from src.api.schemas import Token
from src.db.database import get_db

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
def refresh(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception:
        raise HTTPException(
            status_code=498,
            detail="Invalid Token/ Refresh Token Required",
        )

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    new_refresh_token = Authorize.create_refresh_token(subject=current_user)
    return Token(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="Bearer",
    )


@login_router.post("/restore-password")
async def restore_password(email: str, session: AsyncSession = Depends(get_db)):
    user = await UserCRUD.get_user_by_email(email, session)
    if user:
        try:
            restore_token = generate_reset_password_token()
            email_token[email] = restore_token
            await send_reset_token(email, restore_token)

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
):
    try:
        if (
            email in email_token
            and email_token[email] == token
            and new_password == confirm_password
        ):
            updated_user = await UserCRUD.change_user_password(
                email, new_password, session
            )

            if updated_user:
                del email_token[email]

                return {"message": "password has been changed"}
            else:
                return {"message": "error change"}
        else:
            return {"message": "error"}
    except Exception as e:
        return {"error": f"error {str(e)}"}
