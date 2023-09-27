from fastapi import status
from httpx import AsyncClient

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
