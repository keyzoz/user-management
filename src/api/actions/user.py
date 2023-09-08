from uuid import UUID

from src.api.schemas import ShowUser, UserCreate
from src.db.dals import Roles, UserDAL
from src.db.models import User
from src.hashing import Hasher


async def _create_new_user(body: UserCreate, session) -> ShowUser:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(
            name=body.name,
            surname=body.surname,
            username=body.username,
            phone_number=body.phone_number,
            group_name=body.group_name,
            email=body.email,
            image_s3=body.image_s3,
            hashed_password=Hasher.get_password_hash(body.password),
            role=Roles.USER_USER,
        )
        return ShowUser(
            name=user.name,
            surname=user.surname,
            username=user.username,
            phone_number=user.phone_number,
            email=user.email,
            group_name=user.group_name,
            image_s3=user.image_s3,
            is_blocked=user.is_blocked,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )


async def _update_user(
    updated_user_params: dict, user_id: UUID, session
) -> UUID | None:
    async with session.begin():
        user_dal = UserDAL(session)
        updated_user_id = await user_dal.update_user(
            user_id=user_id, **updated_user_params
        )
        return updated_user_id


async def _get_user_by_id(user_id, session) -> User | None:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_id(user_id=user_id)
        if user is not None:
            return user


async def _delete_user(user_id, session) -> UUID | None:
    async with session.begin():
        user_dal = UserDAL(session)
        deleted_user_id = await user_dal.delete_user(user_id=user_id)
        return deleted_user_id
