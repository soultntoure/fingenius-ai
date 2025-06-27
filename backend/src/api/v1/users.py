from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, List

from ...core.security import get_current_user
from ...models.user import UserRead, UserUpdate
from ...services.user_service import UserService

router = APIRouter()

@router.get("/", response_model=List[UserRead])
async def read_users(user_service: Annotated[UserService, Depends()],
                     current_user: Annotated[UserRead, Depends(get_current_user)]):
    """Retrieve multiple users (admin only, or self for general users)."""
    # Example: if current_user.role != "admin": raise HTTPException(...)
    users = await user_service.get_all_users()
    return users

@router.get("/{user_id}", response_model=UserRead)
async def read_user(user_id: int, user_service: Annotated[UserService, Depends()],
                    current_user: Annotated[UserRead, Depends(get_current_user)]):
    """Retrieve a single user by ID."""
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # Add authorization logic here if user_id is not current_user.id
    return user

@router.put("/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user_update: UserUpdate,
                      user_service: Annotated[UserService, Depends()],
                      current_user: Annotated[UserRead, Depends(get_current_user)]):
    """Update user information."""
    # Add authorization logic: user_id must be current_user.id or admin
    updated_user = await user_service.update_user(user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated_user