from fastapi import APIRouter

from . import auth, users, accounts, transactions, budgets, savings, investments, goals

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(accounts.router, prefix="/accounts", tags=["Accounts"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
api_router.include_router(budgets.router, prefix="/budgets", tags=["Budgets"])
api_router.include_router(savings.router, prefix="/savings", tags=["Savings"])
api_router.include_router(investments.router, prefix="/investments", tags=["Investments"])
api_router.include_router(goals.router, prefix="/goals", tags=["Goals"])