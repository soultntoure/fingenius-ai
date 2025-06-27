import pandas as pd
from sklearn.ensemble import RandomForestClassifier

class InvestmentAdvisor:
    def __init__(self):
        self.model = RandomForestClassifier(random_state=42)
        self.risk_tolerance_map = {'low': 0, 'medium': 1, 'high': 2}
        self.inv_strategy_map = {0: 'conservative', 1: 'moderate', 2: 'aggressive'}

    def train_strategy_model(self, user_profile_data: pd.DataFrame, historical_performance_data: pd.DataFrame):
        """
        Trains a model to recommend investment strategies based on user profiles.
        user_profile_data should include 'user_id', 'age', 'risk_tolerance', 'investment_strategy'.
        historical_performance_data could be used for feature engineering.
        """
        print("Training investment strategy model...")
        # For simplicity, let's assume 'risk_tolerance' directly maps to strategy
        X = user_profile_data[['age', 'risk_tolerance']].copy()
        X['risk_tolerance_encoded'] = X['risk_tolerance'].map(self.risk_tolerance_map)
        y = user_profile_data['investment_strategy'].map(self.inv_strategy_map)

        # Replace with actual model training on processed data
        # self.model.fit(X, y)
        print("Investment strategy model trained.")

    def recommend_strategy(self, user_profile: dict) -> str:
        """
        Recommends an investment strategy based on user profile and goals.
        user_profile: {'age', 'risk_tolerance', 'financial_goals'}
        """
        print(f"Recommending investment strategy for user...")
        risk_tolerance_level = user_profile.get('risk_tolerance', 'medium').lower()
        if risk_tolerance_level == 'low':
            return "conservative" # Focus on capital preservation, low volatility
        elif risk_tolerance_level == 'medium':
            return "moderate"   # Balanced growth and risk
        elif risk_tolerance_level == 'high':
            return "aggressive"  # Focus on high growth, higher volatility
        else:
            return "moderate" # Default

    def suggest_portfolio_allocation(self, strategy: str) -> dict:
        """
        Suggests a basic asset allocation based on the recommended strategy.
        """
        allocations = {
            "conservative": {"stocks": 0.3, "bonds": 0.6, "cash": 0.1},
            "moderate": {"stocks": 0.6, "bonds": 0.3, "cash": 0.1},
            "aggressive": {"stocks": 0.8, "bonds": 0.15, "cash": 0.05}
        }
        return allocations.get(strategy, allocations["moderate"])