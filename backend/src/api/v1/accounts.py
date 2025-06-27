from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, List

from ...core.security import get_current_user
from ...models.financial import AccountRead, AccountCreate, PlaidPublicTokenExchange
from ...services.account_service import AccountService
from ...services.plaid_webhook_handler import PlaidWebhookHandler # Example usage
from ...models.user import UserRead # Assuming UserRead is imported for current_user type hint

router = APIRouter()

@router.post("/", response_model=AccountRead, status_code=status.HTTP_201_CREATED)
async def create_account(account_create: AccountCreate,
                         account_service: Annotated[AccountService, Depends()],
                         current_user: Annotated[UserRead, Depends(get_current_user)]):
    """Connect a new financial account."""
    account = await account_service.create_user_account(current_user.id, account_create)
    return account

@router.get("/", response_model=List[AccountRead])
async def get_user_accounts(account_service: Annotated[AccountService, Depends()],
                            current_user: Annotated[UserRead, Depends(get_current_user)]):
    """Retrieve all financial accounts for the current user."""
    accounts = await account_service.get_accounts_by_user(current_user.id)
    return accounts

@router.post("/plaid/exchange_public_token")
async def exchange_plaid_public_token(token_data: PlaidPublicTokenExchange,
                                       plaid_handler: Annotated[PlaidWebhookHandler, Depends()],
                                       current_user: Annotated[UserRead, Depends(get_current_user)]):
    """Exchange Plaid public token for access token."""
    await plaid_handler.exchange_public_token(token_data.public_token, current_user.id)
    return {"message": "Public token exchanged successfully, accounts linked."}

# Add other CRUD for accounts like update, delete, get by ID