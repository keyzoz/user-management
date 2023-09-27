from fastapi import status
from httpx import AsyncClient

from tests.crud import create_user_and_group_data


async def test_get_user_with_user_role(
    ac: AsyncClient, generate_random_user_data, generate_group_name
):
    data = generate_random_user_data
    password = data[0]
    user_data = data[1]
    group_name = generate_group_name
    user_data["group_name"] = group_name
    await create_user_and_group_data(group_name=group_name, user_data=user_data)

    user_for_login = {
        "username": user_data["username"],
        "password": password,
    }

    login = await ac.post("/auth/token", data=user_for_login)

    data_from_login = login.json()

    assert login.status_code == status.HTTP_200_OK

    resp = await ac.get(
        "/user/{}".format(user_data["user_id"]),
        headers={"Authorization": "Bearer {}".format(data_from_login["access_token"])},
    )

    assert resp.status_code == status.HTTP_403_FORBIDDEN


async def test_patch_user_with_user_role(
    ac: AsyncClient, generate_random_user_data, generate_group_name
):
    data = generate_random_user_data
    password = data[0]
    user_data = data[1]
    group_name = generate_group_name
    user_data["group_name"] = group_name
    user_data["role"] = "USER"
    await create_user_and_group_data(group_name=group_name, user_data=user_data)

    user_for_login = {
        "username": user_data["username"],
        "password": password,
    }

    data_for_patch = {
        "surname": "Slavkin",
        "phone_number": "+37543134531",
        "email": "slavkin2023@example.com",
    }
    login = await ac.post("/auth/token", data=user_for_login)

    data_from_login = login.json()

    assert login.status_code == status.HTTP_200_OK

    headers = {"Authorization": "Bearer {}".format(data_from_login["access_token"])}
    resp = await ac.patch(
        "/user/{}".format(user_data["user_id"]),
        json=data_for_patch,
        headers=headers,
    )

    assert resp.status_code == status.HTTP_403_FORBIDDEN


async def test_patch_user_with_moderator_role(
    ac: AsyncClient, generate_random_moderator_data, generate_group_name
):
    data = generate_random_moderator_data
    password = data[0]
    user_data = data[1]
    group_name = generate_group_name
    user_data["group_name"] = group_name
    await create_user_and_group_data(group_name=group_name, user_data=user_data)

    user_for_login = {
        "username": user_data["username"],
        "password": password,
    }

    data_for_patch = {
        "surname": "Slavkin",
        "phone_number": "+37543134531",
        "email": "slavkin2023@example.com",
    }
    login = await ac.post("/auth/token", data=user_for_login)

    data_from_login = login.json()

    assert login.status_code == status.HTTP_200_OK

    headers = {"Authorization": "Bearer {}".format(data_from_login["access_token"])}
    resp = await ac.patch(
        "/user/{}".format(user_data["user_id"]),
        json=data_for_patch,
        headers=headers,
    )

    assert resp.status_code == status.HTTP_403_FORBIDDEN
