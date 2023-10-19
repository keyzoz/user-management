from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, validator

from settings import SECRET_KEY
from src.api import validators


class TunedModel(BaseModel):
    class Config:
        orm_mode = True


class UserCreate(TunedModel):
    name: str
    surname: str
    username: str
    phone_number: str
    email: EmailStr
    password: str
    group_name: str

    @validator("name")
    def validate_name(cls, value):
        return validators.validate_name(value)

    @validator("surname")
    def validate_surname(cls, value):
        return validators.validate_surname(value)

    @validator("phone_number")
    def validate_phone_number(cls, value):
        return validators.validate_phone_number(value)


class UpdateUser(BaseModel):
    name: str | None = None
    surname: str | None = None
    username: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    image_s3: str | None = None

    @validator("name")
    def validate_name(cls, value):
        return validators.validate_name(value)

    @validator("surname")
    def validate_surname(cls, value):
        return validators.validate_surname(value)

    @validator("phone_number")
    def validate_phone_number(cls, value):
        return validators.validate_phone_number(value)


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
    role: str
    image_s3: str | None
    is_blocked: bool
    created_at: datetime
    updated_at: datetime | None


class HealthCheckResponse(BaseModel):
    status_code: int
    detail: str


class Settings(BaseModel):
    authjwt_secret_key: str = SECRET_KEY
