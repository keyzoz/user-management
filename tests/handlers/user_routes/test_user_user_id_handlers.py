from fastapi import status
from httpx import AsyncClient


async def test_get_user_by_id(ac: AsyncClient):

    user_for_login = {
        "username": "monarch",
        "password": "admin",
    }

    login = await ac.post("/auth/token", data=user_for_login)

    data_from_login = login.json()

    assert login.status_code == status.HTTP_200_OK

    resp = await ac.get(
        "/user/c43df4fa-7131-40ad-9277-339de8303542",
        headers={"Authorization": "Bearer {}".format(data_from_login["access_token"])},
    )

    data_from_resp = resp.json()

    assert resp.status_code == status.HTTP_200_OK
    assert data_from_resp["name"] == "Dmitriy"
    assert data_from_resp["surname"] == "Slav"
    assert data_from_resp["username"] == "dslav"
    assert data_from_resp["phone_number"] == "+37431314534"
    assert data_from_resp["email"] == "dmslav@example.com"
    assert data_from_resp["image_s3"] == "path/img2"
    assert data_from_resp["group_name"] == "Pandas"


async def test_patch_user_by_id(ac: AsyncClient):

    user_for_login = {
        "username": "monarch",
        "password": "admin",
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
        "/user/c43df4fa-7131-40ad-9277-339de8303542",
        json=data_for_patch,
        headers=headers,
    )

    data_from_resp = resp.json()

    assert resp.status_code == status.HTTP_200_OK
    assert data_from_resp["name"] == "Dmitriy"
    assert data_from_resp["surname"] == data_for_patch["surname"]
    assert data_from_resp["username"] == "dslav"
    assert data_from_resp["phone_number"] == data_for_patch["phone_number"]
    assert data_from_resp["email"] == data_for_patch["email"]
    assert data_from_resp["image_s3"] == "path/img2"
    assert data_from_resp["group_name"] == "Pandas"
