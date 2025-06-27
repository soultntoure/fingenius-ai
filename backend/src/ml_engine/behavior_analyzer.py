import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

class BehaviorAnalyzer:
    def __init__(self):
        self.scaler = StandardScaler()
        self.kmeans_model = None

    def analyze_spending_patterns(self, transactions_df: pd.DataFrame, n_clusters: int = 3):
        """
        Analyzes spending patterns using clustering.
        transactions_df should have 'user_id', 'amount', 'category', 'date'.
        Returns user segments or insights.
        """
        if transactions_df.empty:
            return {}

        # Example: Aggregate spending by category per user
        spending_pivot = transactions_df.groupby(['user_id', 'category'])['amount'].sum().unstack(fill_value=0)
        
        # Normalize data
        scaled_data = self.scaler.fit_transform(spending_pivot)

        # Apply KMeans clustering
        self.kmeans_model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = self.kmeans_model.fit_predict(scaled_data)
        
        spending_pivot['cluster'] = clusters
        
        # Return some insights per cluster
        cluster_summary = spending_pivot.groupby('cluster').mean().to_dict('index')
        return cluster_summary

    def get_user_segment(self, user_transactions_df: pd.DataFrame):
        """
        Identifies the segment for a single user.
        """
        if self.kmeans_model is None:
            raise ValueError("Model not trained. Call analyze_spending_patterns() first.")
        
        user_spending = user_transactions_df.groupby('category')['amount'].sum().unstack(fill_value=0)
        # Ensure consistent columns with training data (add missing categories with 0)
        # This is a simplification; in production, you'd handle unseen categories more robustly.
        all_categories = self.scaler.feature_names_in_ # Assuming StandardScaler remembers features
        user_spending = user_spending.reindex(columns=all_categories, fill_value=0)

        scaled_user_data = self.scaler.transform(user_spending)
        user_cluster = self.kmeans_model.predict(scaled_user_data)[0]
        return user_cluster