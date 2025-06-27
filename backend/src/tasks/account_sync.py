from celery import Celery
from ..core.config import settings
from ..services.account_service import AccountService
from ..db.session import async_session_factory
import asyncio
from sqlalchemy.future import select
from ..db.models.account import Account

celery_app = Celery(
    "fingenius_tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

@celery_app.task
def sync_user_accounts_task(user_id: int):
    """
    Celery task to synchronize financial accounts for a given user.
    This would involve calling Plaid's /transactions/get or similar APIs.
    """
    async def _sync_accounts():
        async with async_session_factory() as session:
            account_service = AccountService(session)
            
            # Fetch all accounts for the user
            result = await session.execute(select(Account).where(Account.user_id == user_id))
            accounts = result.scalars().all()

            print(f"Starting account sync for user_id: {user_id} ({len(accounts)} accounts)")
            for account in accounts:
                try:
                    await account_service.sync_transactions_for_account(account.id)
                    # Also update balances if necessary after transaction sync
                    # await account_service.update_account_balances(account.id, new_current_balance, new_available_balance)
                except Exception as e:
                    print(f"Error syncing account {account.id} for user {user_id}: {e}")
            print(f"Account sync for user_id: {user_id} completed.")
    
    # Run the async function using asyncio
    asyncio.run(_sync_accounts())

@celery_app.task
def refresh_all_accounts_periodically():
    """
    Celery task to periodically refresh all active user accounts.
    Scheduled task (e.g., daily).
    """
    async def _refresh_all_accounts():
        async with async_session_factory() as session:
            # In a real app, you'd fetch distinct user_ids with active accounts
            result = await session.execute(select(Account.user_id).distinct())
            active_user_ids = result.scalars().all()

            print(f"Starting periodic refresh of {len(active_user_ids)} active users' accounts...")
            for user_id in active_user_ids:
                sync_user_accounts_task.delay(user_id) # Enqueue individual user sync tasks
            print("Periodic refresh task initiated.")
    
    asyncio.run(_refresh_all_accounts())