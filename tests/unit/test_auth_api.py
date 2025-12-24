import pytest

@pytest.mark.asyncio
async def test_register_and_login(client):
    response = await client.post("/auth/register", json={
        "username": "alice",
        "password": "password123"
    })
    assert response.status_code == 200

    response = await client.post(
        "/auth/login",
        data={"username": "alice", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
