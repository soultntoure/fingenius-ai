from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from ..ml_engine.budget_optimizer import BudgetOptimizer
from ..ml_engine.savings_strategist import SavingsStrategist
from ..services.notification_service import NotificationService
from ..db.models.user import User
import pandas as pd

class AutomationService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.budget_optimizer = BudgetOptimizer()
        self.savings_strategist = SavingsStrategist()
        self.notification_service = NotificationService()

    async def run_daily_automations(self, user_id: int):
        """
        Orchestrates daily AI-driven automation for a given user.
        Fetches data, runs AI models, and proposes actions.
        """
        print(f"Running daily automations for user {user_id}...")

        # 1. Fetch relevant user data (transactions, budgets, goals, etc.)
        # In a real app, this would involve complex DB queries to get historical data
        dummy_transactions_data = {
            'user_id': [user_id, user_id, user_id, user_id],
            'category': ['Groceries', 'Transport', 'Groceries', 'Shopping'],
            'amount': [150.0, 50.0, 120.0, 80.0],
            'date': ["2023-11-01", "2023-11-05", "2023-11-10", "2023-11-15"]
        }
        spending_history_df = pd.DataFrame(dummy_transactions_data)

        dummy_income_data = pd.DataFrame({'user_id': [user_id], 'amount': [3000.0]})
        dummy_expense_data = pd.DataFrame({'user_id': [user_id], 'amount': [1500.0]})
        dummy_goals_data = pd.DataFrame({'user_id': [user_id], 'name': ['Emergency Fund'], 'target_amount': [5000.0], 'current_amount': [1000.0], 'target_date': ["2024-12-31"]})

        current_budget_data = {"Groceries": 100.0, "Transport": 70.0, "Shopping": 50.0}

        # 2. Run AI models
        budget_suggestions = self.budget_optimizer.optimize_budget(user_id, current_budget_data, spending_history_df)
        savings_suggestion = self.savings_strategist.suggest_savings_contribution(user_id, dummy_income_data, dummy_expense_data, dummy_goals_data)
        # investment_strategy_suggestion = self.investment_advisor.recommend_strategy(...) # if implemented

        # 3. Store AI suggestions and mark for user approval
        proposed_actions = []

        # Example: Budget suggestion
        for category, suggestion in budget_suggestions['suggestions'].items():
            if suggestion['action'] != 'no_change':
                proposed_actions.append({
                    "type": "budget_adjustment",
                    "description": f"Adjust {category} budget: {suggestion['action']} to {suggestion['suggested_amount']}",
                    "action_details": {"category": category, **suggestion},
                    "requires_approval": True
                })

        # Example: Savings suggestion
        if savings_suggestion['suggested_amount'] > 0:
            proposed_actions.append({
                "type": "savings_transfer",
                "description": f"Transfer ${savings_suggestion['suggested_amount']} to savings goals.",
                "action_details": {"amount": savings_suggestion['suggested_amount']},
                "requires_approval": True
            })

        # 4. Notify user about pending actions
        if proposed_actions:
            await self.notification_service.notify_automation_pending_approval(
                user_id,
                {"description": f"You have {len(proposed_actions)} new AI-driven financial suggestions awaiting your review."}
            )
            # Store proposed_actions in DB for user to review in Automation Console
            print(f"Proposed {len(proposed_actions)} actions for user {user_id}.")
        else:
            print(f"No significant actions proposed for user {user_id}.")

        return {"message": "Automation run complete.", "proposed_actions": proposed_actions}

    async def approve_action(self, user_id: int, action_id: int):
        """
        Applies an approved automated action.
        """
        print(f"Applying approved action {action_id} for user {user_id}...")
        # Logic to fetch action from DB, verify user ownership, and then execute it
        # e.g., update budget, initiate bank transfer, adjust investment allocation
        print("Action applied.")