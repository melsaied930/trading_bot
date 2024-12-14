# backtest/backtest_engine.py

import pandas as pd
import time


class BacktestEngine:
    def __init__(self, strategy, data_file="data/historical_data.csv"):
        self.data_file = data_file
        self.strategy = strategy
        self.data = None

    def load_data(self):
        """Load historical data from a CSV file."""
        self.data = pd.read_csv(self.data_file, parse_dates=["timestamp"])
        print(f"Loaded {len(self.data)} rows of historical data.")

    def run_backtest(self):
        """Run backtest on historical data."""
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")

        for index, row in self.data.iterrows():
            price = row["close"]
            timestamp = row["timestamp"]

            # Simulate data feeding
            decision = self.strategy.make_decision(price)
            if decision in ["BUY", "SELL"]:
                self.strategy.place_order("AAPL", decision, price, timestamp)

            time.sleep(0.01)  # Simulate processing delay

        print("Backtest Completed.")
