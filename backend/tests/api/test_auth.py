import pytest
from httpx import AsyncClient
from backend.src.main import app # Assuming main is accessible for testing

@pytest.mark.asyncio
async def test_register_user_success():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/auth/register",
            json={"email": "test@example.com", "username": "testuser", "password": "password123", "full_name": "Test User"}
        )
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["email"] == "test@example.com"

@pytest.mark.asyncio
async def test_register_user_duplicate_email():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Register once
        await ac.post(
            "/api/v1/auth/register",
            json={"email": "duplicate@example.com", "username": "dupuser", "password": "password123", "full_name": "Dup User"}
        )
        # Try to register again with same email
        response = await ac.post(
            "/api/v1/auth/register",
            json={"email": "duplicate@example.com", "username": "anotheruser", "password": "password123", "full_name": "Another User"}
        )
    assert response.status_code == 409 # Conflict
    assert "User with this email or username already exists" in response.json()["detail"]

@pytest.mark.asyncio
async def test_login_for_access_token_success():
    # First, register a user
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post(
            "/api/v1/auth/register",
            json={"email": "login@example.com", "username": "loginuser", "password": "securepassword", "full_name": "Login User"}
        )
    
    # Then, attempt to log in
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/auth/login",
            data={
                "username": "loginuser",
                "password": "securepassword"
            }
        )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_for_access_token_invalid_credentials():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/auth/login",
            data={
                "username": "nonexistent",
                "password": "wrongpass"
            }
        )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]