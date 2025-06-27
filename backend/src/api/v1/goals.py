from fastapi import APIRouter, Depends
from typing import List, Annotated
from ...core.security import get_current_user
from ...models.financial import GoalRead, GoalCreate # Assuming Goal models exist

router = APIRouter()

@router.get("/", response_model=List[GoalRead])
async def get_goals(current_user: Annotated[dict, Depends(get_current_user)]):
    """Retrieve financial goals for the authenticated user."""
    return []

@router.post("/", response_model=GoalRead)
async def create_goal(goal: GoalCreate, current_user: Annotated[dict, Depends(get_current_user)]):
    """Create a new financial goal."""
    return GoalRead(id=1, name=goal.name, target_amount=goal.target_amount, current_amount=0.0)