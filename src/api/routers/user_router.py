from logging import getLogger
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.actions.user import UserCRUD
from src.api.schemas import (DeleteUserResponse, ShowUser, UpdateUser,
                             UserCreate)
from src.db.database import get_db
from src.permissons import (is_admin_or_moderator_of_target_group,
                            is_moderator_of_target_group_or_admin)

logger = getLogger(__name__)

user_router = APIRouter()


@user_router.post("/signup", response_model=ShowUser)
async def create_user(body: UserCreate, session: AsyncSession = Depends(get_db)):
    try:
        return await UserCRUD.create_new_user(body, session)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@user_router.patch("/me")
async def update_current_user(
    body: UpdateUser,
    Authorize: AuthJWT = Depends(),
    session: AsyncSession = Depends(get_db),
) -> ShowUser:
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=498, detail="Invalid Token")
    updated_user_params = body.dict(exclude_none=True)
    cur_user_username = Authorize.get_jwt_subject()
    if cur_user_username is None:
        raise HTTPException(status_code=404, detail=f"User not found.")
    if updated_user_params == {}:
        raise HTTPException(
            status_code=422,
            detail=f"At least one parameter for user update info should be provided",
        )
    try:
        user = await UserCRUD.get_user_by_username(cur_user_username, session)
        await UserCRUD.update_user(
            updated_user_params=updated_user_params,
            session=session,
            user_id=user.user_id,
        )
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return user


@user_router.get("/me")
async def get_current_user(
    Authorize: AuthJWT = Depends(),
    session: AsyncSession = Depends(get_db),
) -> ShowUser:
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=498, detail="Invalid Token")
    cur_user_username = Authorize.get_jwt_subject()
    if cur_user_username is None:
        raise HTTPException(status_code=404, detail=f"User not found.")
    user = await UserCRUD.get_user_by_username(cur_user_username, session)
    return user


@user_router.delete("/me")
async def delete_current_user(
    Authorize: AuthJWT = Depends(),
    session: AsyncSession = Depends(get_db),
) -> DeleteUserResponse:
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=498, detail="Invalid Token")
    cur_user_username = Authorize.get_jwt_subject()
    if cur_user_username is None:
        raise HTTPException(status_code=404, detail=f"User not found.")
    user = await UserCRUD.get_user_by_username(cur_user_username, session)
    deleted_user_id = await UserCRUD.delete_user(user.user_id, session)
    return DeleteUserResponse(deleted_user_id=deleted_user_id)


@user_router.patch("/{user_id}")
async def update_user_by_id(
    user_id: UUID,
    body: UpdateUser,
    Authorize: AuthJWT = Depends(),
    session: AsyncSession = Depends(get_db),
) -> ShowUser:
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=498, detail="Invalid Token")
    updated_user_params = body.dict(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(
            status_code=422,
            detail=f"At least one parameter for user update info should be provided",
        )

    user = await UserCRUD.get_user_by_id(user_id, session)
    cur_user = await UserCRUD.get_user_by_username(Authorize.get_jwt_subject(), session)
    if not is_moderator_of_target_group_or_admin(cur_user, user):
        raise HTTPException(status_code=403, detail="Forbidden")
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    try:
        await UserCRUD.update_user(
            updated_user_params=updated_user_params, session=session, user_id=user_id
        )
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return user


@user_router.get("/{user_id}")
async def get_user_by_id(
    user_id: UUID,
    Authorize: AuthJWT = Depends(),
    session: AsyncSession = Depends(get_db),
) -> ShowUser:
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=498, detail="Invalid Token")
    user = await UserCRUD.get_user_by_id(user_id, session)
    cur_user = await UserCRUD.get_user_by_username(Authorize.get_jwt_subject(), session)
    if not is_admin_or_moderator_of_target_group(cur_user, user):
        raise HTTPException(status_code=403, detail="Forbidden")
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    return user
