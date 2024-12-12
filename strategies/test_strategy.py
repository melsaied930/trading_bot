# strategies/test_strategy.py

from data.data_fetcher import DataFetcher
from brokers.broker_api import BrokerAPI
import time


class TestStrategy:
    def __init__(self):
        # Moved Configuration
        self.fetcher = DataFetcher()
        self.broker = BrokerAPI()

        # Trading Configurations
        self.stock_symbol = "NVDA"   # Stock Symbol
        self.quantity = 100          # Trade Quantity
        self.fetch_interval = 1      # Fetch Interval in Seconds

        # Trading Logic Timers
        self.last_buy_time = 0
        self.buy_interval = 10       # Buy every 10 seconds
        self.sell_delay = 5          # Sell after 5 seconds
        self.holding_position = False

    def fetch_live_data(self):
        """Fetch live market data using the configured fetcher."""
        return self.fetcher.fetch_live_data(self.stock_symbol)

    def make_decision(self, price):
        """Make trading decisions based on the configured timing."""
        current_time = time.time()

        # Buy Logic: Every 10 seconds
        if not self.holding_position and (current_time - self.last_buy_time >= self.buy_interval):
            self.last_buy_time = current_time
            self.holding_position = True
            print("Decision: BUY")
            return "BUY"

        # Sell Logic: Sell 5 seconds after the last buy
        if self.holding_position and (current_time - self.last_buy_time >= self.sell_delay):
            self.holding_position = False
            print("Decision: SELL")
            return "SELL"

        print("Decision: HOLD")
        return "HOLD"

    def place_order(self, symbol, side, price):
        """Place orders with the broker."""
        try:
            order_ref = f"Order-{int(time.time())}"
            self.broker.place_order(symbol, side, self.quantity, order_ref)
            print(f"Order Executed: {side} {self.quantity} of {symbol} at {price}")
        except Exception as e:
            print(f"Order Placement Error: {e}")

    def run_bot(self):
        """Main Execution Loop Moved Here."""
        while True:
            try:
                # Fetch live market data
                data = self.fetch_live_data()
                print(f"Fetched Data: {data}")

                # Make trading decision
                decision = self.make_decision(data['price'])

                if decision in ["BUY", "SELL"]:
                    self.place_order(data['symbol'], decision, data['price'])
                    print(f"Order Executed: {decision} at {data['price']}")

                time.sleep(self.fetch_interval)
            except Exception as e:
                print(f"Error: {e}")
