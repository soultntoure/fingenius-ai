import pandas as pd
from sklearn.linear_model import LinearRegression

class BudgetOptimizer:
    def __init__(self):
        self.model = LinearRegression()

    def optimize_budget(self, user_id: int, current_budget_data: dict, spending_history_df: pd.DataFrame) -> dict:
        """
        Analyzes spending history and financial goals to suggest budget adjustments.
        Returns optimized budget suggestions.
        current_budget_data: {'category': limit}
        spending_history_df: pd.DataFrame with 'user_id', 'category', 'amount', 'date'
        """
        print(f"Optimizing budget for user {user_id}...")
        
        # Filter for the specific user's spending history
        user_spending = spending_history_df[spending_history_df['user_id'] == user_id]

        if user_spending.empty:
            return {"message": "No spending history for optimization", "suggestions": current_budget_data}

        # Example: Simple optimization based on average spending vs budget
        # This is a simplified approach. A real model would use more features and time-series analysis.
        category_spending_avg = user_spending.groupby('category')['amount'].mean()

        optimized_budget_suggestions = {}
        for category, limit in current_budget_data.items():
            avg_spent = category_spending_avg.get(category, 0)
            if avg_spent > limit * 1.1: # If overspent by more than 10%
                optimized_budget_suggestions[category] = {
                    "action": "decrease_suggestion",
                    "suggested_amount": round(avg_spent * 0.9, 2), # Suggesting 10% less than average spent
                    "reason": "Consistently overspending in this category."
                }
            elif avg_spent < limit * 0.8: # If underspent by more than 20%
                 optimized_budget_suggestions[category] = {
                    "action": "increase_suggestion",
                    "suggested_amount": round(avg_spent * 1.1, 2), # Suggesting 10% more than average spent
                    "reason": "Consistently underspending; consider reallocating funds."
                }
            else:
                optimized_budget_suggestions[category] = {"action": "no_change", "reason": "Spending within healthy limits."}

        return {"message": "Budget optimization initiated", "suggestions": optimized_budget_suggestions}
