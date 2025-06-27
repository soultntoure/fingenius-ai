from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..session import Base

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    plaid_transaction_id = Column(String, index=True, nullable=True) # Optional, for Plaid transactions
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    category = Column(String, nullable=True)
    type = Column(String, nullable=False) # 'debit', 'credit'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="transactions")
    account = relationship("Account", back_populates="transactions")