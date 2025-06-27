from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..db.models.account import Account
from ..models.financial import AccountCreate, AccountRead, PlaidAccountData
from ..core.exceptions import NotFoundException
from plaid import PlaidApi, Environment
from plaid.model.transactions_sync_request import TransactionsSyncRequest

class AccountService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        # Plaid client initialization (simplified)
        # self.plaid_client = PlaidApi(
        #     Environment.Sandbox,
        #     client_id="YOUR_PLAID_CLIENT_ID",
        #     secret="YOUR_PLAID_SECRET"
        # )

    async def create_user_account(self, user_id: int, account_in: AccountCreate) -> AccountRead:
        # This would likely involve exchanging public token via Plaid API first
        # For now, a dummy create
        db_account = Account(
            user_id=user_id,
            plaid_account_id="dummy_plaid_acc_id",
            plaid_item_id="dummy_plaid_item_id",
            access_token="encrypted_plaid_access_token", # Should be encrypted
            name=account_in.name,
            official_name=account_in.official_name,
            subtype=account_in.subtype,
            type=account_in.type,
            current_balance=0.0,
            available_balance=0.0,
            iso_currency_code=account_in.iso_currency_code or "USD"
        )
        self.db_session.add(db_account)
        await self.db_session.commit()
        await self.db_session.refresh(db_account)
        return AccountRead.model_validate(db_account)

    async def get_accounts_by_user(self, user_id: int) -> List[AccountRead]:
        result = await self.db_session.execute(
            select(Account).where(Account.user_id == user_id)
        )
        accounts = result.scalars().all()
        return [AccountRead.model_validate(acc) for acc in accounts]
    
    async def sync_transactions_for_account(self, account_id: int):
        """
        Synchronizes transactions for a specific account using Plaid.
        """
        db_account = await self.db_session.get(Account, account_id)
        if not db_account:
            raise NotFoundException(detail="Account not found.")
        
        # Placeholder for Plaid API call
        # request = TransactionsSyncRequest(access_token=db_account.access_token)
        # response = self.plaid_client.transactions_sync(request)
        # new_transactions = response.get('added', [])
        # For each new transaction, create a Transaction DB entry
        print(f"Syncing transactions for account: {db_account.name} (ID: {account_id})")
        # Logic to save new transactions, update existing ones, etc.
        await self.db_session.commit()
        print("Transactions synced.")