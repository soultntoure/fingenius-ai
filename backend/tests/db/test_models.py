import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date

from backend.src.db.session import Base # Import Base from your session.py
from backend.src.db.models.user import User
from backend.src.db.models.account import Account
from backend.src.db.models.transaction import Transaction
from backend.src.db.models.budget import Budget
from backend.src.db.models.saving import Saving
from backend.src.db.models.investment import Investment
from backend.src.db.models.goal import Goal

# Use an in-memory SQLite database for testing
@pytest.fixture(name="db_session")
async def create_db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    AsyncSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
async def test_create_user(db_session: AsyncSession):
    user = User(username="testuser", email="test@example.com", hashed_password="hashedpassword")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.is_active is True

@pytest.mark.asyncio
async def test_create_account_and_link_to_user(db_session: AsyncSession):
    user = User(username="accountuser", email="account@example.com", hashed_password="pass")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    account = Account(
        user_id=user.id,
        plaid_account_id="plaid_acc_123",
        plaid_item_id="plaid_item_abc",
        access_token="access_token_encrypted",
        name="Checking Account",
        type="depository",
        current_balance=1000.50,
        available_balance=950.00,
        iso_currency_code="USD"
    )
    db_session.add(account)
    await db_session.commit()
    await db_session.refresh(account)

    assert account.id is not None
    assert account.user_id == user.id
    assert account.name == "Checking Account"

    # Verify relationship
    await db_session.refresh(user, attribute_names=["accounts"])
    assert len(user.accounts) == 1
    assert user.accounts[0].name == "Checking Account"

@pytest.mark.asyncio
async def test_create_transaction(db_session: AsyncSession):
    user = User(username="txuser", email="tx@example.com", hashed_password="pass")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    account = Account(
        user_id=user.id, plaid_account_id="plaid_acc_456", plaid_item_id="plaid_item_def",
        access_token="token", name="Savings", type="depository"
    )
    db_session.add(account)
    await db_session.commit()
    await db_session.refresh(account)

    transaction_date = datetime.utcnow()
    transaction = Transaction(
        user_id=user.id,
        account_id=account.id,
        description="Grocery Store",
        amount=55.75,
        date=transaction_date,
        category="Groceries",
        type="debit"
    )
    db_session.add(transaction)
    await db_session.commit()
    await db_session.refresh(transaction)

    assert transaction.id is not None
    assert transaction.description == "Grocery Store"
    assert transaction.amount == 55.75
    assert transaction.date.day == transaction_date.day
    assert transaction.user_id == user.id
    assert transaction.account_id == account.id

    # Verify relationships
    await db_session.refresh(user, attribute_names=["transactions"])
    await db_session.refresh(account, attribute_names=["transactions"])
    assert len(user.transactions) == 1
    assert len(account.transactions) == 1

@pytest.mark.asyncio
async def test_create_budget(db_session: AsyncSession):
    user = User(username="budgetuser", email="budget@example.com", hashed_password="pass")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    budget = Budget(
        user_id=user.id,
        category="Food",
        amount=300.00,
        period="monthly",
        current_spent=50.00
    )
    db_session.add(budget)
    await db_session.commit()
    await db_session.refresh(budget)

    assert budget.id is not None
    assert budget.category == "Food"
    assert budget.amount == 300.00
    assert budget.user_id == user.id

@pytest.mark.asyncio
async def test_create_saving_goal(db_session: AsyncSession):
    user = User(username="savinguser", email="saving@example.com", hashed_password="pass")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    saving = Saving(
        user_id=user.id,
        name="New Car Fund",
        target_amount=25000.00,
        current_amount=500.00,
        target_date=datetime(2025, 12, 31)
    )
    db_session.add(saving)
    await db_session.commit()
    await db_session.refresh(saving)

    assert saving.id is not None
    assert saving.name == "New Car Fund"
    assert saving.target_amount == 25000.00
    assert saving.user_id == user.id

@pytest.mark.asyncio
async def test_create_investment(db_session: AsyncSession):
    user = User(username="investuser", email="invest@example.com", hashed_password="pass")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    investment = Investment(
        user_id=user.id,
        name="Vanguard S&P 500 ETF",
        type="ETF",
        current_value=1200.50,
        initial_investment=1000.00,
        acquisition_date=datetime(2023, 1, 15)
    )
    db_session.add(investment)
    await db_session.commit()
    await db_session.refresh(investment)

    assert investment.id is not None
    assert investment.name == "Vanguard S&P 500 ETF"
    assert investment.type == "ETF"
    assert investment.user_id == user.id

@pytest.mark.asyncio
async def test_create_goal(db_session: AsyncSession):
    user = User(username="goaluser", email="goal@example.com", hashed_password="pass")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    goal = Goal(
        user_id=user.id,
        name="Emergency Fund",
        description="Build a 6-month emergency fund",
        target_amount=10000.00,
        current_amount=2500.00,
        target_date=datetime(2024, 6, 30),
        priority="high",
        status="active"
    )
    db_session.add(goal)
    await db_session.commit()
    await db_session.refresh(goal)

    assert goal.id is not None
    assert goal.name == "Emergency Fund"
    assert goal.target_amount == 10000.00
    assert goal.status == "active"