from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Annotated

from ...core.security import get_current_user
from ...models.auth import Token, LoginSchema
from ...models.user import UserRead, UserCreate
from ...services.user_service import UserService

router = APIRouter()

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user_create: UserCreate, user_service: Annotated[UserService, Depends()]):
    """Register a new user."""
    user = await user_service.create_user(user_create)
    return user

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: LoginSchema, user_service: Annotated[UserService, Depends()]):
    """Login and get an access token."""
    user = await user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = user_service.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserRead)
async def read_users_me(current_user: Annotated[UserRead, Depends(get_current_user)]):
    """Get current user's profile."""
    return current_user