import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
import joblib # For model persistence

class TransactionCategorizer:
    def __init__(self):
        self.model = None
        self.label_encoder = LabelEncoder()
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(stop_words='english', max_features=1000)),
            ('classifier', LogisticRegression(max_iter=1000))
        ])

    def train(self, transactions_df: pd.DataFrame):
        """
        Trains the categorization model.
        transactions_df should have 'description' and 'category' columns.
        """
        # Encode categories
        self.label_encoder.fit(transactions_df['category'])
        y_encoded = self.label_encoder.transform(transactions_df['category'])

        # Train pipeline
        self.pipeline.fit(transactions_df['description'], y_encoded)
        self.model = self.pipeline # The pipeline is our model

    def predict(self, description: str) -> str:
        """
        Predicts the category for a given transaction description.
        """
        if self.model is None:
            raise ValueError("Model not trained. Call .train() first.")
        prediction_encoded = self.model.predict([description])
        return self.label_encoder.inverse_transform(prediction_encoded)[0]

    def save_model(self, path: str):
        joblib.dump(self.model, path + '_model.pkl')
        joblib.dump(self.label_encoder, path + '_encoder.pkl')

    def load_model(self, path: str):
        self.model = joblib.load(path + '_model.pkl')
        self.label_encoder = joblib.load(path + '_encoder.pkl')

# Example usage (in a script, not production code)
if __name__ == "__main__":
    data = {
        'description': [
            'STARBUCKS COFFEE', 'WHOLE FOODS MARKET', 'AMAZON.COM',
            'NYC TRANSIT MTA', 'ATM WITHDRAWAL', 'UBER TRIP',
            'Spotify Premium', 'Netflix Subscription'
        ],
        'category': [
            'Coffee', 'Groceries', 'Shopping',
            'Transportation', 'Cash', 'Transportation',
            'Subscriptions', 'Subscriptions'
        ]
    }
    df = pd.DataFrame(data)

    categorizer = TransactionCategorizer()
    categorizer.train(df)

    print(f"Predicted: {categorizer.predict('DUNKIN DONUTS')}")
    print(f"Predicted: {categorizer.predict('TRADER JOES')}")
    print(f"Predicted: {categorizer.predict('GOOGLE PLAY')}")