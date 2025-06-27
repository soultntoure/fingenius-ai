from sqlalchemy.ext.asyncio import AsyncSession
from ..db.models.account import Account
from ..core.exceptions import NotFoundException
from plaid import PlaidApi, Environment
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from ..core.config import settings

class PlaidWebhookHandler:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.plaid_client = PlaidApi(
            Environment[settings.PLAID_ENV.upper()],
            client_id=settings.PLAID_CLIENT_ID,
            secret=settings.PLAID_SECRET
        )

    async def exchange_public_token(self, public_token: str, user_id: int):
        """
        Exchanges a Plaid public token for an access token and links accounts.
        """
        print(f"Exchanging public token for user {user_id}...")
        try:
            exchange_request = ItemPublicTokenExchangeRequest(
                public_token=public_token
            )
            exchange_response = await self.plaid_client.item_public_token_exchange(exchange_request)
            access_token = exchange_response.access_token
            item_id = exchange_response.item_id

            # Normally, you'd fetch initial accounts/transactions here too
            # For MVP, just store access token and item_id for a dummy account
            # In a real app, this would involve more detailed Plaid API calls

            # Create a dummy account record, this needs to be properly linked/updated
            # with actual Plaid account data (fetched via /accounts/get)
            # This is a simplification:
            db_account = Account(
                user_id=user_id,
                plaid_account_id=f"dummy_acc_{item_id}", # Needs actual account ID from Plaid /accounts/get
                plaid_item_id=item_id,
                access_token=access_token, # Store encrypted in production
                name=f"Plaid Linked Account ({item_id[-4:]})",
                type="depository",
                iso_currency_code="USD"
            )
            self.db_session.add(db_account)
            await self.db_session.commit()
            await self.db_session.refresh(db_account)
            print(f"Public token exchanged and item {item_id} linked for user {user_id}.")

        except Exception as e:
            print(f"Error exchanging public token: {e}")
            raise

    async def handle_webhook(self, webhook_data: dict):
        """
        Handles incoming Plaid webhooks (e.g., SYNC_UPDATES, DEFAULT_UPDATE).
        Parses webhook and triggers appropriate background tasks (e.g., account sync).
        """
        print(f"Received Plaid webhook: {webhook_data.get('webhook_code')} for item {webhook_data.get('item_id')}")
        item_id = webhook_data.get('item_id')
        webhook_type = webhook_data.get('webhook_type')
        webhook_code = webhook_data.get('webhook_code')

        if webhook_type == "TRANSACTIONS" and webhook_code == "DEFAULT_UPDATE":
            # Trigger transaction sync for the affected item_id
            # Find the user associated with this item_id
            # db_account = await self.db_session.execute(select(Account).filter_by(plaid_item_id=item_id)).scalar_one_or_none()
            # if db_account:
            #   from ..tasks.account_sync import sync_user_accounts_task
            #   sync_user_accounts_task.delay(db_account.user_id)
            print(f"Triggering transaction sync for item {item_id}")
        # Add logic for other webhook types (e.g., item_error, auth_updates, investments_updates)
