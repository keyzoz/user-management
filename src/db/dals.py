from uuid import UUID

from sqlalchemy import and_, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Roles, User


class UserDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
        self,
        name: str,
        surname: str,
        username: str,
        phone_number: str,
        email: str,
        hashed_password: str,
        group_name: str,
        role=Roles,
    ) -> User:
        new_user = User(
            name=name,
            surname=surname,
            username=username,
            phone_number=phone_number,
            email=email,
            role=role,
            hashed_password=hashed_password,
            group_name=group_name,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def delete_user(self, user_id: UUID) -> UUID | None:
        query = delete(User).where(User.user_id == user_id)
        res = await self.db_session.execute(query)
        return user_id

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        query = select(User).where(User.user_id == user_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def get_user_by_username(self, username: str) -> User | None:
        query = select(User).where(User.username == username)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def get_user_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def update_user(self, user_id=UUID, **kwargs) -> UUID | None:
        query = (
            update(User)
            .where(and_(User.user_id == user_id, User.is_blocked == False))
            .values(kwargs)
            .returning(User.user_id)
        )
        res = await self.db_session.execute(query)
        update_user_row = res.fetchone()
        if update_user_row is not None:
            return update_user_row[0]

    async def update_user_password(
        self, email: str, hashed_password: str
    ) -> UUID | None:
        query = (
            update(User)
            .where(and_(User.email == email, User.is_blocked == False))
            .values(hashed_password=hashed_password)
            .returning(User.user_id)
        )
        res = await self.db_session.execute(query)
        update_user_row = res.fetchone()
        if update_user_row is not None:
            return update_user_row[0]

    async def update_user_photo(self, username: str, image_s3: str) -> User | None:
        query = (
            update(User)
            .where(and_(User.username == username, User.is_blocked == False))
            .values(image_s3=image_s3)
            .returning(User)
        )
        res = await self.db_session.execute(query)
        update_user_row = res.fetchone()
        if update_user_row is not None:
            return update_user_row[0]

    async def get_user_with_query_params(
        self,
        page: int = 1,
        limit: int = 30,
        filter_by_name: str = None,
        sort_by: str = None,
        order_by: str = "asc",
        group_name: str = None,
    ):
        if filter_by_name:
            query = select(User).where(User.name == filter_by_name)
        else:
            query = select(User)
        if group_name:
            query = query.where(User.group_name == group_name)
        if sort_by:
            order_clause = getattr(User, sort_by)

            if order_by == "desc":
                order_clause = order_clause.desc()
            query = query.order_by(order_clause)

        query = query.offset((page - 1) * limit).limit(limit)

        res = await self.db_session.execute(query)
        users = res.scalars().all()

        return users
