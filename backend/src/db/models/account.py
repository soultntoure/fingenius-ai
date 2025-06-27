from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..session import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plaid_account_id = Column(String, index=True, nullable=False, unique=True) # ID from Plaid
    plaid_item_id = Column(String, index=True, nullable=False) # Item ID from Plaid
    access_token = Column(String, nullable=False) # Encrypted Plaid access token
    name = Column(String, nullable=False)
    official_name = Column(String, nullable=True)
    subtype = Column(String, nullable=True)
    type = Column(String, nullable=False) # e.g., depository, credit
    current_balance = Column(Float, nullable=True)
    available_balance = Column(Float, nullable=True)
    iso_currency_code = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")

    def __repr__(self):
        return f"<Account(id={self.id}, name='{self.name}', user_id={self.user_id})>"