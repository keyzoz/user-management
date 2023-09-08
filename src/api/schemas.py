import re
from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, validator

VALIDATE_USER_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    class Config:
        orm_mode = True


class UserCreate(TunedModel):
    name: str
    surname: str
    username: str
    phone_number: str
    email: EmailStr
    image_s3: str
    password: str
    group_name: str


class UpdateUser(BaseModel):
    name: str | None = None
    surname: str | None = None
    username: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    image_s3: str | None = None

    @validator("name")
    def validate_name(cls, value):
        if not VALIDATE_USER_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value

    @validator("surname")
    def validate_surname(cls, value):
        if not VALIDATE_USER_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Surname should contains only letters"
            )
        return value


class DeleteUserResponse(BaseModel):
    deleted_user_id: UUID


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class ShowUser(TunedModel):
    name: str
    surname: str
    username: str
    phone_number: str
    group_name: str
    email: EmailStr
    image_s3: str
    is_blocked: bool
    created_at: datetime
    updated_at: datetime | None


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
