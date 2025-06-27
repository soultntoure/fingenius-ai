from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class AccountBase(BaseModel):
    name: str
    official_name: Optional[str] = None
    type: str # e.g., 'depository', 'credit'
    subtype: Optional[str] = None
    iso_currency_code: Optional[str] = "USD"

class AccountCreate(AccountBase):
    pass

class AccountRead(AccountBase):
    id: int
    user_id: int
    plaid_account_id: str
    plaid_item_id: str
    current_balance: Optional[float] = None
    available_balance: Optional[float] = None

    class Config:
        from_attributes = True

class TransactionBase(BaseModel):
    description: str
    amount: float
    date: date
    category: Optional[str] = None
    type: str # 'debit', 'credit'
    account_id: int

class TransactionCreate(TransactionBase):
    pass

class TransactionRead(TransactionBase):
    id: int
    user_id: Optional[int] = None # Will be populated by service
    plaid_transaction_id: Optional[str] = None

    class Config:
        from_attributes = True

class BudgetBase(BaseModel):
    category: str
    amount: float
    period: str # e.g., 'monthly', 'weekly'

class BudgetCreate(BudgetBase):
    pass

class BudgetRead(BudgetBase):
    id: int
    user_id: Optional[int] = None

    class Config:
        from_attributes = True

class SavingBase(BaseModel):
    name: str
    target_amount: float
    current_amount: Optional[float] = 0.0
    target_date: Optional[date] = None

class SavingCreate(SavingBase):
    pass

class SavingRead(SavingBase):
    id: int
    user_id: Optional[int] = None

    class Config:
        from_attributes = True

class InvestmentBase(BaseModel):
    name: str
    type: str
    current_value: float
    initial_investment: Optional[float] = None
    acquisition_date: Optional[date] = None

class InvestmentCreate(InvestmentBase):
    pass

class InvestmentRead(InvestmentBase):
    id: int
    user_id: Optional[int] = None

    class Config:
        from_attributes = True

class GoalBase(BaseModel):
    name: str
    description: Optional[str] = None
    target_amount: float
    current_amount: Optional[float] = 0.0
    target_date: Optional[date] = None
    priority: Optional[str] = None
    status: Optional[str] = "active"

class GoalCreate(GoalBase):
    pass

class GoalRead(GoalBase):
    id: int
    user_id: Optional[int] = None

    class Config:
        from_attributes = True

class PlaidPublicTokenExchange(BaseModel):
    public_token: str