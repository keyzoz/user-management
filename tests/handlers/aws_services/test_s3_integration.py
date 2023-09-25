import io

from fastapi import UploadFile, status
from httpx import AsyncClient

from tests.conftest import generate_group_name, generate_random_user_data
from tests.crud import create_user_and_group_data


async def test_upload_photo(ac: AsyncClient):
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
    fake_file = UploadFile(io.BytesIO(b"fsdfsdfsdfsdfsdf"))
    file_content = fake_file.file.read()
    assert login.status_code == status.HTTP_200_OK

    resp_d = await ac.post(
        "/user/upload-photo",
        data={"file": file_content},
        headers={
            "Authorization": "Bearer {}".format(
                data_from_login["access_token"],
            )
        },
    )

    assert resp_d.json() == {"message": "Tdsfsdf"}
