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
        self.fetch_interval = 30  # Log every 30 seconds
        self.price_history = []

    def fetch_live_data(self):
        """Fetch live market data every 30 seconds."""
        data = self.fetcher.fetch_live_data(self.stock_symbol)

        # Debug: Print fetched data structure
        print(f"Fetched Data: {data}")

        # Validate the fetched data structure
        if not isinstance(data, dict):
            raise KeyError("Fetched data is not a dictionary.")

        required_keys = ['last_close', 'current_open']
        missing_keys = [key for key in required_keys if key not in data]

        if missing_keys:
            raise KeyError(f"Missing required data keys: {missing_keys}")

        return data

    def place_order(self, symbol, side, price):
        """Place orders with the broker."""
        try:
            order_ref = f"Order-{int(time.time())}"
            self.broker.place_order(symbol, side, self.quantity, order_ref)
            print(f"Order Executed: {side} {self.quantity} of {symbol} at {price}")
        except Exception as e:
            print(f"Order Placement Error: {e}")

    def calculate_ema(self, prices, period=21):
        """Calculate the EMA for the prices list."""
        if len(prices) < period:
            return None  # Not enough data to calculate EMA
        multiplier = 2 / (period + 1)
        ema = prices[0]
        for price in prices[1:]:
            ema = (price - ema) * multiplier + ema
        return ema

    def log_market_data(self, last_close, current_open, ema):
        """Log market data details."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        ema_display = f"{ema:.2f}" if ema else "N/A"
        print(f"[{timestamp}] Last Close: {last_close}, Current Open: {current_open}, EMA 21: {ema_display}")

    def run_bot(self):
        """Log close price, open price, and EMA 21 every 30 seconds."""
        while True:
            try:
                # Fetch live market data
                data = self.fetch_live_data()
                last_close = data['last_close']
                current_open = data['current_open']

                # Update price history
                self.price_history.append(last_close)
                if len(self.price_history) > 21:
                    self.price_history.pop(0)

                # Calculate EMA
                ema = self.calculate_ema(self.price_history)

                # Log the market data
                self.log_market_data(last_close, current_open, ema)

                # Wait for the next fetch interval
                time.sleep(self.fetch_interval)
            except KeyError as ke:
                print(f"Data Fetch Error: {ke}")
            except Exception as e:
                print(f"Unexpected Error: {e}")
