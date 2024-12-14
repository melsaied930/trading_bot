# **Trading Strategy for AAPL (Every Minute)**
#
# ### **Trading Conditions**
# 1. **Long Position:**
# - Buy 10 shares of AAPL when:
# - The last minute's closing price is above the EMA 10.
# - The current minute's opening price is also above the EMA 10.
#
# 2. **Short Position:**
# - Sell short 10 shares of AAPL when:
# - The last minute's closing price is below the EMA 10.
# - The current minute's opening price is also below the EMA 10.
#
# ---
#
# ### **Risk Management**
# - **Position Closure Rule:**
# - Close all current positions before switching trading directions (from long to short or vice versa).
#
# ---
#
# ### **Logging Transactions**
# - Record the following details for every transaction:
#     - **Timestamp:** Date and time of the trade.
#     - **Action:** Buy or sell (long or short).
#     - **Quantity:** Number of shares traded (always 10).
#     - **Price:** Execution price.
#     - **Reason:** Trigger condition met (above/below EMA 10).
#     - **Profit/Loss:** Calculate the P/L for closed trades.
#
# ---








from data.data_fetcher import DataFetcher
from brokers.broker_api import BrokerAPI
import time


class Strategy:
    def __init__(self):
        # Initialize fetcher and broker
        self.fetcher = DataFetcher()
        self.broker = BrokerAPI()
        self.stock_symbol = "AAPL"
        self.fetch_interval = 30  # Check every 30 seconds
        self.price_history = [274.80]  # Start EMA from 274.80
        self.current_ema = 274.80  # Set initial EMA to 274.80
        self.current_position = None
        self.quantity = 10

    def fetch_live_data(self):
        """Fetch live market data."""
        data = self.fetcher.fetch_live_data(self.stock_symbol)

        # Validate fetched data structure
        if not isinstance(data, dict):
            raise KeyError("Fetched data is not a dictionary.")

        required_keys = ['last_close', 'current_open']
        missing_keys = [key for key in required_keys if key not in data]

        if missing_keys:
            raise KeyError(f"Missing required data keys: {missing_keys}")

        return data

    def calculate_ema(self, new_price, period=10):
        """Calculate the EMA with the new price."""
        multiplier = 2 / (period + 1)
        self.current_ema = (new_price - self.current_ema) * multiplier + self.current_ema
        return self.current_ema

    def place_order(self, side, price, reason):
        """Place orders with the broker."""
        try:
            order_ref = f"Order-{int(time.time())}"
            self.broker.place_order(self.stock_symbol, side, self.quantity, order_ref)
            print(f"Order Executed: {side} {self.quantity} of {self.stock_symbol} at {price}")
            self.log_transaction(side, price, reason)
        except Exception as e:
            print(f"Order Placement Error: {e}")

    def log_transaction(self, action, price, reason):
        """Log transaction details."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        print(f"[{timestamp}] Action: {action}, Quantity: {self.quantity}, Price: {price}, Reason: {reason}")

    def make_decision(self, last_close, current_open):
        """Make trading decisions based on the defined strategy."""
        if last_close > self.current_ema and current_open > self.current_ema and self.current_position != "LONG":
            self.place_order("BUY", current_open, "Above EMA 10")
            self.current_position = "LONG"
        elif last_close < self.current_ema and current_open < self.current_ema and self.current_position != "SHORT":
            self.place_order("SELL", current_open, "Below EMA 10")
            self.current_position = "SHORT"

    def run_bot(self):
        """Execute trading strategy every 30 seconds."""
        while True:
            try:
                # Fetch live market data
                data = self.fetch_live_data()
                last_close = data['last_close']
                current_open = data['current_open']

                # Update price history
                self.price_history.append(last_close)
                if len(self.price_history) > 10:
                    self.price_history.pop(0)

                # Calculate updated EMA
                updated_ema = self.calculate_ema(last_close)

                # Make trading decision
                self.make_decision(last_close, current_open)

                print(f"Updated EMA 10: {updated_ema:.2f}")

                # Wait for the next fetch interval
                time.sleep(self.fetch_interval)

            except KeyError as ke:
                print(f"Data Fetch Error: {ke}")
            except Exception as e:
                print(f"Unexpected Error: {e}")
