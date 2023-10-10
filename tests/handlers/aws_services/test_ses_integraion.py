from fastapi import status
from httpx import AsyncClient

from src.api.actions.token import ResetTokenService
from src.db.redis_db import get_redis_client
from tests.crud import create_user_and_group_data


async def test_sent_reset_link_valid_email(
    ac: AsyncClient, generate_group_name, generate_random_user_data
):
    data = generate_random_user_data
    user_data = data[1]
    group_name = generate_group_name
    user_data["group_name"] = group_name
    await create_user_and_group_data(group_name=group_name, user_data=user_data)

    valid_email = {"email": user_data["email"]}

    resp_d = await ac.post("/auth/sent-reset-link", params=valid_email)
    assert resp_d.status_code == status.HTTP_200_OK
    assert resp_d.json() == {"message": "The token has been sent"}


async def test_sent_reset_link_invalid_email(ac: AsyncClient):

    invalid_email = {"email": "us@example.com"}

    resp_d = await ac.post("/auth/sent-reset-link", params=invalid_email)
    assert resp_d.status_code == status.HTTP_404_NOT_FOUND
    assert resp_d.json() == {"detail": "Email has not found"}


async def test_reset_password(
    ac: AsyncClient, redis_client, generate_group_name, generate_random_user_data
):
    data = generate_random_user_data
    user_data = data[1]
    group_name = generate_group_name
    user_data["group_name"] = group_name
    await create_user_and_group_data(group_name=group_name, user_data=user_data)

    valid_token = "token"
    valid_email = user_data["email"]

    reset_token_service = ResetTokenService()
    reset_token_service.redis_storage = redis_client
    reset_token_service.send_reset_token(reset_token=valid_token, email=valid_email)
    reset_token_service.store_reset_token(token=valid_token, email=valid_email)

    params = {
        "email": valid_email,
        "token": valid_token,
        "new_password": "password",
        "confirm_password": "password",
    }

    resp = await ac.post("/auth/reset-password", params=params)

    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == {"message": "Password has been changed"}


async def test_reset_password_with_invalid_token(
    ac: AsyncClient, redis_client, generate_group_name, generate_random_user_data
):
    data = generate_random_user_data
    user_data = data[1]
    group_name = generate_group_name
    user_data["group_name"] = group_name
    await create_user_and_group_data(group_name=group_name, user_data=user_data)

    valid_token = "token"
    valid_email = user_data["email"]

    reset_token_service = ResetTokenService()
    reset_token_service.redis_storage = redis_client
    reset_token_service.send_reset_token(reset_token=valid_token, email=valid_email)
    reset_token_service.store_reset_token(token=valid_token, email=valid_email)

    params = {
        "email": valid_email,
        "token": "invalid token",
        "new_password": "password",
        "confirm_password": "password",
    }

    resp = await ac.post("/auth/reset-password", params=params)

    assert resp.status_code == 200
    assert resp.json() == {"message": "Invalid token or password"}
