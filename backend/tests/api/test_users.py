import pytest
from httpx import AsyncClient
from backend.src.main import app
from backend.src.core.security import create_access_token
from datetime import timedelta

@pytest.fixture
def auth_headers():
    # Create a dummy token for testing authenticated endpoints
    token = create_access_token({"sub": "test_authenticated@example.com"}, expires_delta=timedelta(minutes=5))
    return {"Authorization": f"Bearer {token}"}

@pytest.mark.asyncio
async def test_read_users_me(auth_headers):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/auth/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == "test_authenticated@example.com"

@pytest.mark.asyncio
async def test_read_users_unauthenticated():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/auth/me")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_update_user_profile(auth_headers):
    # First, register a user to ensure it exists and can be updated
    async with AsyncClient(app=app, base_url="http://test") as ac:
        reg_response = await ac.post(
            "/api/v1/auth/register",
            json={"email": "update_me@example.com", "username": "updateme", "password": "oldpass", "full_name": "Old Name"}
        )
        user_id = reg_response.json()["id"]
    
    # Now, test update endpoint (assuming user_id 1 is the authenticated user for simplicity in test setup)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put(
            f"/api/v1/users/{user_id}", # In real app, only authenticated user can update their own profile
            json={"full_name": "New Full Name", "password": "newsecurepass"},
            headers=auth_headers
        )
    assert response.status_code == 200
    assert response.json()["full_name"] == "New Full Name"
    assert response.json()["email"] == "test_authenticated@example.com" # Email from token, not from user in DB

