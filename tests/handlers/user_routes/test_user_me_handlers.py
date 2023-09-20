from fastapi import status
from httpx import AsyncClient


async def test_get_user_me(ac: AsyncClient):

    user_for_login = {
        "username": "alexlost21",
        "password": "string",
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


async def test_patch_user_me(ac: AsyncClient):

    user_data = {
        "name": "Alex",
        "surname": "Lost",
        "username": "alexlost21",
        "phone_number": "+79525024142",
        "email": "alex21@example.com",
        "image_s3": "string",
        "password": "string",
        "group_name": "Pandas",
    }

    user_for_login = {
        "username": "alexlost21",
        "password": "string",
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


async def test_delete_user_me(ac: AsyncClient):
    user_for_login = {
        "username": "vic",
        "password": "admin",
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
    assert resp.json() == {"deleted_user_id": "e23df4fa-7331-40cd-9277-339de8303542"}
