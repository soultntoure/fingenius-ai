import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from backend.src.db.session import Base
from backend.src.services.user_service import UserService
from backend.src.models.user import UserCreate, UserUpdate
from backend.src.core.exceptions import UserAlreadyExists

# In-memory SQLite for fast, isolated tests
@pytest.fixture(name="db_session")
async def create_db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, autocommit=False, autoflush=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
async def test_create_user(db_session: AsyncSession):
    user_service = UserService(db_session)
    user_create = UserCreate(username="testuser", email="test@example.com", password="securepass123")
    user_read = await user_service.create_user(user_create)

    assert user_read.username == "testuser"
    assert user_read.email == "test@example.com"
    assert user_read.id is not None

@pytest.mark.asyncio
async def test_create_user_duplicate_email(db_session: AsyncSession):
    user_service = UserService(db_session)
    user_create1 = UserCreate(username="user1", email="duplicate@example.com", password="pass1")
    await user_service.create_user(user_create1)

    user_create2 = UserCreate(username="user2", email="duplicate@example.com", password="pass2")
    with pytest.raises(UserAlreadyExists):
        await user_service.create_user(user_create2)

@pytest.mark.asyncio
async def test_get_user_by_email(db_session: AsyncSession):
    user_service = UserService(db_session)
    user_create = UserCreate(username="findme", email="findme@example.com", password="pass")
    await user_service.create_user(user_create)

    found_user = await user_service.get_user_by_email("findme@example.com")
    assert found_user is not None
    assert found_user.email == "findme@example.com"

    not_found_user = await user_service.get_user_by_email("nonexistent@example.com")
    assert not_found_user is None

@pytest.mark.asyncio
async def test_update_user(db_session: AsyncSession):
    user_service = UserService(db_session)
    user_create = UserCreate(username="updateuser", email="update@example.com", password="oldpass")
    created_user = await user_service.create_user(user_create)

    user_update = UserUpdate(full_name="Updated Name", password="newpass")
    updated_user = await user_service.update_user(created_user.id, user_update)

    assert updated_user is not None
    assert updated_user.full_name == "Updated Name"
    # Verify password change (by trying to authenticate with new password)
    authenticated_user = await user_service.authenticate_user(updated_user.email, "newpass")
    assert authenticated_user is not None
    assert authenticated_user.id == updated_user.id

@pytest.mark.asyncio
async def test_authenticate_user(db_session: AsyncSession):
    user_service = UserService(db_session)
    user_create = UserCreate(username="authuser", email="auth@example.com", password="supersecret")
    await user_service.create_user(user_create)

    # Test successful authentication
    authenticated = await user_service.authenticate_user("auth@example.com", "supersecret")
    assert authenticated is not None
    assert authenticated.email == "auth@example.com"

    # Test wrong password
    failed_auth = await user_service.authenticate_user("auth@example.com", "wrongsecret")
    assert failed_auth is None

    # Test non-existent user
    failed_auth_nonexistent = await user_service.authenticate_user("noone@example.com", "anypass")
    assert failed_auth_nonexistent is None