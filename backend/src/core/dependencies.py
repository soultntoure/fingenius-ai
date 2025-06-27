from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.session import async_session_factory
from fastapi import Depends

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency that provides an async database session."""
    async with async_session_factory() as session:
        yield session

# Example for services:
from ..services.user_service import UserService
from ..services.account_service import AccountService
# ... other services

def get_user_service(session: AsyncSession = Depends(get_db_session)) -> UserService:
    return UserService(session)

def get_account_service(session: AsyncSession = Depends(get_db_session)) -> AccountService:
    return AccountService(session)

# ... other get_service functions