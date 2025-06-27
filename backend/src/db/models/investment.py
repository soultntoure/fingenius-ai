from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..session import Base

class Investment(Base):
    __tablename__ = "investments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False) # e.g., 'Vanguard Total Stock Market Index Fund'
    type = Column(String, nullable=False) # e.g., 'stock', 'bond', 'mutual_fund', 'crypto'
    current_value = Column(Float, nullable=False)
    initial_investment = Column(Float, nullable=False)
    acquisition_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="investments")