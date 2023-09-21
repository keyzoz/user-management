from httpx import AsyncClient


async def test_sent_reset_link_valid_email(ac: AsyncClient):

    valid_email = "test@example.com"

    resp = await ac.post("/auth/sent-reset-link", json=valid_email)

    assert resp.status_code == 200
