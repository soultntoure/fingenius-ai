from fastapi import APIRouter, Depends
from typing import List, Annotated
from ...core.security import get_current_user
from ...models.financial import BudgetRead, BudgetCreate

router = APIRouter()

@router.get("/", response_model=List[BudgetRead])
async def get_budgets(current_user: Annotated[dict, Depends(get_current_user)]):
    """Retrieve budgets for the authenticated user."""
    return []

@router.post("/", response_model=BudgetRead)
async def create_budget(budget: BudgetCreate, current_user: Annotated[dict, Depends(get_current_user)]):
    """Create a new budget."""
    return BudgetRead(id=1, category=budget.category, amount=budget.amount, period="monthly")