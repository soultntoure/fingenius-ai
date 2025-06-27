import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

class FinancialForecaster:
    def __init__(self):
        self.models = {}

    def train_cash_flow_forecast_model(self, user_id: int, transaction_data: pd.DataFrame):
        """
        Trains a time-series model (e.g., ARIMA) for cash flow forecasting.
        transaction_data: pd.DataFrame with 'date', 'amount', 'type' (debit/credit), 'user_id'
        """
        print(f"Training cash flow forecast model for user {user_id}...")
        user_transactions = transaction_data[transaction_data['user_id'] == user_id].copy()
        if user_transactions.empty or len(user_transactions) < 20: # Need enough data points
            print(f"Not enough data for user {user_id} to train forecasting model.")
            return
        
        # Prepare data: sum daily net cash flow
        user_transactions['date'] = pd.to_datetime(user_transactions['date'])
        user_transactions['net_amount'] = user_transactions.apply(lambda row: row['amount'] if row['type'] == 'credit' else -row['amount'], axis=1)
        daily_cash_flow = user_transactions.groupby('date')['net_amount'].sum().resample('D').sum().fillna(0)

        try:
            # Example ARIMA model (p,d,q). This might need tuning.
            model = ARIMA(daily_cash_flow, order=(5,1,0))
            model_fit = model.fit()
            self.models[user_id] = model_fit
            print(f"Cash flow forecast model trained for user {user_id}.")
        except Exception as e:
            print(f"Error training ARIMA model for user {user_id}: {e}")

    def forecast_cash_flow(self, user_id: int, steps: int = 30) -> list:
        """
        Generates a cash flow forecast for the specified number of future steps (days).
        """
        if user_id not in self.models:
            print(f"No trained model found for user {user_id}. Cannot forecast.")
            return []
        
        model_fit = self.models[user_id]
        forecast = model_fit.predict(start=len(model_fit.fittedvalues), end=len(model_fit.fittedvalues) + steps - 1)
        
        # Convert forecast to a list of dicts for API response
        forecast_data = []
        current_date = model_fit.index[-1] + pd.Timedelta(days=1)
        for val in forecast:
            forecast_data.append({"date": current_date.strftime("%Y-%m-%d"), "net_cash_flow": round(val, 2)})
            current_date += pd.Timedelta(days=1)

        return forecast_data
