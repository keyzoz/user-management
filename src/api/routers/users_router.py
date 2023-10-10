from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.actions.user import UserCRUD
from src.api.schemas import ShowUser
from src.db.database import get_db
from src.permissons import is_admin, is_moderator

users_router = APIRouter()


@users_router.get("/users", response_model=List[ShowUser])
async def get_users(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=30, ge=1, le=100),
    filter_by_name: str = Query(default=None),
    sort_by: str = Query(default=None),
    order_by: str = Query(default="asc"),
    session: AsyncSession = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=498, detail="Invalid Token")
    cur_user = await UserCRUD.get_user_by_username(Authorize.get_jwt_subject(), session)
    if not is_admin(cur_user) and not is_moderator(cur_user):
        raise HTTPException(status_code=403, detail="Forbidden")
    group_name = None if is_admin(cur_user) else cur_user.group_name
    users = await UserCRUD.get_users_by_query_params(
        page=page,
        limit=limit,
        filter_by_name=filter_by_name,
        sort_by=sort_by,
        order_by=order_by,
        session=session,
        group_name=group_name,
    )

    return users
