import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.models.transaction import Transaction
from ..db.models.account import Account
from datetime import datetime

class DataIngestionService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def ingest_transactions_from_plaid(self, user_id: int, account_id: int, transactions_data: list):
        """
        Ingests raw transaction data from Plaid and stores it in the database.
        Performs basic data cleaning and transformation.
        """
        print(f"Ingesting {len(transactions_data)} transactions for account {account_id}...")
        new_transactions = []
        for tx_data in transactions_data:
            # Basic validation and transformation
            try:
                tx = Transaction(
                    user_id=user_id,
                    account_id=account_id,
                    plaid_transaction_id=tx_data.get('transaction_id'),
                    description=tx_data.get('name', 'N/A'),
                    amount=tx_data.get('amount'), # Plaid amounts are usually positive for debits, negative for credits
                    date=datetime.strptime(tx_data.get('date'), '%Y-%m-%d'),
                    category=tx_data.get('personal_finance_category', {}).get('primary') or tx_data.get('category', ['Uncategorized'])[0],
                    type='debit' if tx_data.get('amount', 0) > 0 else 'credit' # Adjust based on Plaid's convention
                )
                new_transactions.append(tx)
            except Exception as e:
                print(f"Skipping invalid transaction data: {tx_data} - Error: {e}")

        if new_transactions:
            self.db_session.add_all(new_transactions)
            await self.db_session.commit()
            print(f"Successfully ingested {len(new_transactions)} new transactions.")
        else:
            print("No valid transactions to ingest.")

    async def update_account_balances(self, account_id: int, current_balance: float, available_balance: float):
        """
        Updates the balance information for a given account.
        """
        account = await self.db_session.get(Account, account_id)
        if account:
            account.current_balance = current_balance
            account.available_balance = available_balance
            await self.db_session.commit()
            print(f"Updated balance for account {account_id}: Current={current_balance}, Available={available_balance}")
        else:
            print(f"Account {account_id} not found for balance update.")
