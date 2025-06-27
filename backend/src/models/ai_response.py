from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class AISuggestion(BaseModel):
    type: str # e.g., "budget_adjustment", "savings_transfer", "investment_rebalance"
    description: str
    action_details: Dict[str, Any]
    confidence_score: Optional[float] = None
    requires_approval: bool = True

class AIAnalysisReport(BaseModel):
    analysis_type: str # e.g., "spending_behavior", "financial_health"
    summary: str
    insights: List[str]
    recommendations: List[AISuggestion]
    generated_at: str # ISO format date-time