from fastapi import status
from httpx import AsyncClient

from tests.crud import create_user_and_group_data


async def test_upload_photo(
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

    resp_d = await ac.post(
        "/user/upload-photo",
        files={"file": open("tests/img.png", "rb")},
        headers={
            "Authorization": "Bearer {}".format(
                data_from_login["access_token"],
            )
        },
    )

    data_from_update = resp_d.json()
    assert resp_d.status_code == 200
    assert data_from_update["username"] == user_data["username"]
    assert data_from_update["image_s3"] is not None
