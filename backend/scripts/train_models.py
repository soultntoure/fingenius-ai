import pandas as pd
import os
from backend.src.ml_engine.transaction_categorizer import TransactionCategorizer
# Import other ML models as needed

def run_training():
    """
    Script to train all necessary ML models for the FinGenius AI backend.
    In a real scenario, this would load data from a database or data lake.
    """
    print("Starting ML model training process...")

    # Ensure a 'models' directory exists for saving models
    model_dir = "./backend/models"
    os.makedirs(model_dir, exist_ok=True)

    # --- Transaction Categorizer ---
    print("Training Transaction Categorizer...")
    # Dummy data for demonstration. Replace with actual data loading.
    transaction_data = {
        'description': [
            'STARBUCKS COFFEE', 'WHOLE FOODS MARKET', 'AMAZON.COM',
            'NYC TRANSIT MTA', 'ATM WITHDRAWAL', 'UBER TRIP',
            'Spotify Premium', 'Netflix Subscription', 'Chevron Gas',
            'Target', 'Walmart', 'Shell Gas Station', 'Local Cafe',
            'Online Clothing Store', 'Pharmacy', 'Restaurant Dinner'
        ],
        'category': [
            'Coffee', 'Groceries', 'Shopping',
            'Transportation', 'Cash', 'Transportation',
            'Subscriptions', 'Subscriptions', 'Gas',
            'Shopping', 'Groceries', 'Gas', 'Coffee',
            'Shopping', 'Health', 'Dining Out'
        ]
    }
    transactions_df = pd.DataFrame(transaction_data)
    categorizer = TransactionCategorizer()
    categorizer.train(transactions_df)
    categorizer.save_model(os.path.join(model_dir, "transaction_categorizer"))
    print("Transaction Categorizer trained and saved.")

    # --- Other models would follow similar pattern ---
    # Example for BehaviorAnalyzer (needs more complex data setup):
    # print("Training Behavior Analyzer...")
    # behavior_data = pd.DataFrame({ ... })
    # analyzer = BehaviorAnalyzer()
    # analyzer.train_model(behavior_data)
    # analyzer.save_model(os.path.join(model_dir, "behavior_analyzer"))
    # print("Behavior Analyzer trained and saved.")

    print("All ML models training completed successfully.")

if __name__ == "__main__":
    run_training()