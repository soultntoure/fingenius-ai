import pandas as pd

class SavingsStrategist:
    def __init__(self):
        pass

    def suggest_savings_contribution(self, user_id: int, income_data: pd.DataFrame, expense_data: pd.DataFrame, goals_data: pd.DataFrame) -> dict:
        """
        Analyzes user income, expenses, and savings goals to suggest optimal savings contributions.
        """
        print(f"Suggesting savings contribution for user {user_id}...")
        
        # Placeholder logic: simple calculation based on disposable income
        # In a real scenario, this would involve more sophisticated forecasting and goal prioritization.
        
        total_income = income_data[income_data['user_id'] == user_id]['amount'].sum()
        total_expenses = expense_data[expense_data['user_id'] == user_id]['amount'].sum()
        
        disposable_income = total_income - total_expenses
        
        suggested_amount = 0.0
        if disposable_income > 0:
            # Try to save 20% of disposable income, or what's needed for nearest goal
            suggested_amount = disposable_income * 0.20
        
        # Prioritize goals
        # closest_goal = goals_data[goals_data['user_id'] == user_id].sort_values(by='target_date').iloc[0]
        # remaining_for_goal = closest_goal['target_amount'] - closest_goal['current_amount']
        # suggested_amount = min(suggested_amount, remaining_for_goal)

        return {"message": "Savings suggestion generated", "suggested_amount": round(max(0, suggested_amount), 2)}
