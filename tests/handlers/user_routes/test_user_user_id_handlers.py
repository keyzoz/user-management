from fastapi import status
from httpx import AsyncClient

from tests.crud import create_user_and_group_data


async def test_get_user_by_id(
    ac: AsyncClient, generate_random_user_data, generate_group_name
):
    password = generate_random_user_data[0]
    user_data = generate_random_user_data[1]
    group_name = generate_group_name["group_name"]
    user_data["group_name"] = group_name
    user_data["role"] = "ADMIN"
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

    data_from_resp = resp.json()

    assert resp.status_code == status.HTTP_200_OK
    assert data_from_resp["name"] == user_data["name"]
    assert data_from_resp["surname"] == user_data["surname"]
    assert data_from_resp["username"] == user_data["username"]
    assert data_from_resp["phone_number"] == user_data["phone_number"]
    assert data_from_resp["email"] == user_data["email"]
    assert data_from_resp["image_s3"] == user_data["image_s3"]
    assert data_from_resp["group_name"] == user_data["group_name"]


async def test_patch_user_by_id(
    ac: AsyncClient, generate_random_user_data, generate_group_name
):
    password = generate_random_user_data[0]
    user_data = generate_random_user_data[1]
    group_name = generate_group_name["group_name"]
    user_data["group_name"] = group_name
    user_data["role"] = "ADMIN"
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

    data_from_resp = resp.json()

    assert resp.status_code == status.HTTP_200_OK
    assert data_from_resp["name"] == user_data["name"]
    assert data_from_resp["surname"] == data_for_patch["surname"]
    assert data_from_resp["username"] == user_data["username"]
    assert data_from_resp["phone_number"] == data_for_patch["phone_number"]
    assert data_from_resp["email"] == data_for_patch["email"]
    assert data_from_resp["image_s3"] == user_data["image_s3"]
    assert data_from_resp["group_name"] == user_data["group_name"]
