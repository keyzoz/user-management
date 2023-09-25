from fastapi import status
from httpx import AsyncClient

from tests.conftest import generate_group_name, generate_random_user_data
from tests.crud import (create_only_group_data, create_only_user_data,
                        create_user_and_group_data)


async def test_get_user_with_admin_role(
    ac: AsyncClient,
):
    admin_user_data = generate_random_user_data()
    password = admin_user_data[0]
    user_data = admin_user_data[1]
    group_name = generate_group_name()
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

    assert resp.status_code == status.HTTP_200_OK


async def test_get_user_from_other_group_with_admin_role(ac: AsyncClient):
    data1 = generate_random_user_data()
    password = data1[0]
    user_data1 = data1[1]
    group_name1 = generate_group_name()
    user_data1["group_name"] = group_name1
    user_data1["role"] = "ADMIN"
    await create_user_and_group_data(group_name=group_name1, user_data=user_data1)

    data2 = generate_random_user_data()
    user_data2 = data2[1]
    group_name2 = generate_group_name()
    user_data2["group_name"] = group_name2
    user_data2["role"] = "USER"
    await create_user_and_group_data(group_name=group_name2, user_data=user_data2)

    user_for_login = {
        "username": user_data1["username"],
        "password": password,
    }

    login = await ac.post("/auth/token", data=user_for_login)

    data_from_login = login.json()

    assert login.status_code == status.HTTP_200_OK

    resp = await ac.get(
        "/user/{}".format(user_data2["user_id"]),
        headers={"Authorization": "Bearer {}".format(data_from_login["access_token"])},
    )

    assert resp.status_code == status.HTTP_403_FORBIDDEN


async def test_get_users_with_admin_role(
    ac: AsyncClient,
):
    admin_user_data = generate_random_user_data()
    password = admin_user_data[0]
    user_data = admin_user_data[1]
    group_name = generate_group_name()
    user_data["group_name"] = group_name
    user_data["role"] = "ADMIN"
    await create_user_and_group_data(group_name=group_name, user_data=user_data)

    users_data = [generate_random_user_data()[1] for _ in range(5)]
    group_name_other_users = generate_group_name()
    await create_only_group_data(group_name=group_name_other_users)

    for i in range(2):
        users_data[i]["group_name"] = group_name
        users_data[i]["role"] = "USER"
        await create_only_user_data(user_data=users_data[i])

    for i in range(3, 5):
        users_data[i]["group_name"] = group_name_other_users
        users_data[i]["role"] = "MODERATOR"
        await create_only_user_data(user_data=users_data[i])

    user_for_login = {
        "username": user_data["username"],
        "password": password,
    }

    login = await ac.post("/auth/token", data=user_for_login)

    data_from_login = login.json()

    assert login.status_code == status.HTTP_200_OK

    params = {"page": 1, "limit": 5, "sort_by": "name", "order_by": "desc"}

    resp = await ac.get(
        "/users",
        headers={"Authorization": "Bearer {}".format(data_from_login["access_token"])},
        params=params,
    )

    data_from_resp = resp.json()
    assert resp.status_code == status.HTTP_200_OK
    assert len(data_from_resp) == 5
