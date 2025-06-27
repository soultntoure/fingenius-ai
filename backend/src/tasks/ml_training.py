from celery import Celery
from ..core.config import settings
from ..ml_engine.transaction_categorizer import TransactionCategorizer
from ..ml_engine.behavior_analyzer import BehaviorAnalyzer
from ..db.session import async_session_factory
from sqlalchemy.future import select
from ..db.models.transaction import Transaction # Assuming a Transaction model
from ..db.models.user import User # Assuming a User model
import asyncio
import pandas as pd
import os

celery_app = Celery(
    "fingenius_tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

@celery_app.task
def train_transaction_categorizer_task():
    """
    Celery task to train or retrain the transaction categorization model.
    Should be triggered periodically or on significant user corrections.
    """
    async def _train():
        async with async_session_factory() as session:
            print("Fetching transaction data for categorizer training...")
            # Fetch transactions with known categories from DB
            # This would ideally be a dedicated dataset or user-corrected transactions
            result = await session.execute(select(Transaction.description, Transaction.category).filter(Transaction.category.isnot(None)))
            transactions_data = result.all()
            
            if not transactions_data:
                print("No data available for categorizer training.")
                return

            df = pd.DataFrame(transactions_data, columns=['description', 'category'])
            categorizer = TransactionCategorizer()
            categorizer.train(df)
            
            model_dir = "./backend/models"
            os.makedirs(model_dir, exist_ok=True)
            categorizer.save_model(os.path.join(model_dir, "transaction_categorizer"))
            print("Transaction categorizer model trained and saved.")

    asyncio.run(_train())

@celery_app.task
def analyze_user_behavior_task(user_id: int):
    """
    Celery task to run behavioral analysis for a specific user.
    """
    async def _analyze():
        async with async_session_factory() as session:
            print(f"Analyzing behavior for user {user_id}...")
            # Fetch user's transaction history
            result = await session.execute(
                select(Transaction.category, Transaction.amount, Transaction.date)
                .filter(Transaction.user_id == user_id)
            )
            user_transactions = result.all()
            
            if not user_transactions:
                print(f"No transaction data for user {user_id} to analyze.")
                return

            df = pd.DataFrame(user_transactions, columns=['category', 'amount', 'date'])
            df['user_id'] = user_id # Add user_id column for the analyzer
            
            analyzer = BehaviorAnalyzer()
            # This would typically save insights to the DB or trigger other automations
            insights = analyzer.analyze_spending_patterns(df)
            print(f"Behavioral analysis for user {user_id} completed: {insights}")

    asyncio.run(_analyze())

@celery_app.task
def periodic_ml_tasks():
    """
    A meta-task to trigger various ML-related background jobs periodically.
    """
    print("Running periodic ML tasks...")
    train_transaction_categorizer_task.delay()
    
    async def _get_all_users():
        async with async_session_factory() as session:
            result = await session.execute(select(User.id))
            user_ids = result.scalars().all()
            for user_id in user_ids:
                analyze_user_behavior_task.delay(user_id) # Trigger individual user analysis
    
    asyncio.run(_get_all_users())
    print("Periodic ML tasks initiated.")