from fastapi import status
from httpx import AsyncClient

from tests.conftest import generate_group_name, generate_random_user_data
from tests.crud import create_user_and_group_data


async def test_get_user_me(ac: AsyncClient):
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

    login = await ac.post("/auth/token", data=user_for_login)

    data_from_login = login.json()

    assert login.status_code == status.HTTP_200_OK

    resp = await ac.get(
        "/user/me",
        headers={"Authorization": "Bearer {}".format(data_from_login["access_token"])},
    )

    data_from_resp = resp.json()

    assert resp.status_code == status.HTTP_200_OK
    assert data_from_resp["username"] == user_for_login["username"]


async def test_patch_user_me(
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

    data_for_patch = {"surname": "Malkov", "phone_number": "+375291047592"}
    login = await ac.post("/auth/token", data=user_for_login)

    data_from_login = login.json()

    assert login.status_code == status.HTTP_200_OK

    resp = await ac.patch(
        "/user/me",
        json=data_for_patch,
        headers={
            "Authorization": "Bearer {}".format(
                data_from_login["access_token"],
            )
        },
    )

    data_from_resp = resp.json()
    assert resp.status_code == status.HTTP_200_OK
    assert data_from_resp["name"] == user_data["name"]
    assert data_from_resp["surname"] == data_for_patch["surname"]
    assert data_from_resp["username"] == user_data["username"]
    assert data_from_resp["phone_number"] == data_for_patch["phone_number"]
    assert data_from_resp["image_s3"] == user_data["image_s3"]
    assert data_from_resp["group_name"] == user_data["group_name"]


async def test_delete_user_me(
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

    login = await ac.post("/auth/token", data=user_for_login)

    data_from_login = login.json()

    assert login.status_code == status.HTTP_200_OK

    resp = await ac.delete(
        "/user/me",
        headers={
            "Authorization": "Bearer {}".format(
                data_from_login["access_token"],
            )
        },
    )

    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == {"deleted_user_id": user_data["user_id"]}
