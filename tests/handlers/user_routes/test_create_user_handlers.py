from fastapi import status
from httpx import AsyncClient

from tests.conftest import generate_group_name
from tests.crud import create_only_group_data


async def test_create_user(ac: AsyncClient, generate_data_for_signup):
    group_name = generate_group_name()
    await create_only_group_data(group_name=group_name)
    user_data = generate_data_for_signup
    user_data["group_name"] = group_name

    resp = await ac.post("/user/signup", json=user_data)

    data_from_resp = resp.json()
    assert resp.status_code == status.HTTP_200_OK
    assert data_from_resp["name"] == user_data["name"]
    assert data_from_resp["surname"] == user_data["surname"]
    assert data_from_resp["username"] == user_data["username"]
    assert data_from_resp["phone_number"] == user_data["phone_number"]
    assert data_from_resp["image_s3"] is None
    assert data_from_resp["group_name"] == user_data["group_name"]
