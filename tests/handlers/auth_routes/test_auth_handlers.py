from httpx import AsyncClient

from tests.conftest import generate_group_name, generate_random_user_data
from tests.crud import create_user_and_group_data


async def test_login_user(
    ac: AsyncClient,
):
    data = generate_random_user_data()
    password = data[0]
    user_data = data[1]
    group_name = generate_group_name()
    user_data["group_name"] = group_name
    user_data["role"] = "USER"
    await create_user_and_group_data(group_name=group_name, user_data=user_data)

    user_for_login = {
        "username": user_data["username"],
        "password": password,
    }

    resp = await ac.post("/auth/token", data=user_for_login)

    data_from_resp = resp.json()

    assert "access_token" in data_from_resp
    assert "refresh_token" in data_from_resp
    assert data_from_resp["token_type"] == "Bearer"
