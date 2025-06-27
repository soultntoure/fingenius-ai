from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..db.models.user import User
from ..models.user import UserCreate, UserRead, UserUpdate
from ..core.security import get_password_hash, verify_password
from ..core.exceptions import UserAlreadyExists
from ..core.config import settings
from datetime import timedelta

class UserService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, user_in: UserCreate) -> UserRead:
        # Check if user already exists
        result = await self.db_session.execute(
            select(User).where((User.email == user_in.email) | (User.username == user_in.username))
        )
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise UserAlreadyExists()

        hashed_password = get_password_hash(user_in.password)
        db_user = User(
            username=user_in.username,
            email=user_in.email,
            hashed_password=hashed_password,
            full_name=user_in.full_name
        )
        self.db_session.add(db_user)
        await self.db_session.commit()
        await self.db_session.refresh(db_user)
        return UserRead.model_validate(db_user)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.db_session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: int) -> Optional[UserRead]:
        result = await self.db_session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        return UserRead.model_validate(user) if user else None

    async def get_all_users(self) -> List[UserRead]:
        result = await self.db_session.execute(select(User))
        users = result.scalars().all()
        return [UserRead.model_validate(user) for user in users]

    async def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[UserRead]:
        result = await self.db_session.execute(select(User).where(User.id == user_id))
        db_user = result.scalar_one_or_none()
        if not db_user:
            return None
        
        update_data = user_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if key == "password" and value:
                db_user.hashed_password = get_password_hash(value)
            else:
                setattr(db_user, key, value)
        
        await self.db_session.commit()
        await self.db_session.refresh(db_user)
        return UserRead.model_validate(db_user)

    async def authenticate_user(self, username_or_email: str, password: str) -> Optional[User]:
        stmt = select(User).where((User.username == username_or_email) | (User.email == username_or_email))
        result = await self.db_session.execute(stmt)
        user = result.scalar_one_or_none()
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    def create_access_token(self, data: dict):
        return create_access_token(data, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))