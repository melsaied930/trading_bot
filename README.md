# Trading Bot Project Documentation

## **Project Overview**
This project is a fully functional trading bot built using Python. It integrates with the **Interactive Brokers API (IBKR)** using the `ib_insync` library for real-time trading, order execution, and market data retrieval.

### **Key Features:**
- **Automated Market Data Fetching:** Retrieves live market data using the IBKR API.
- **Trading Strategies:** Includes a moving average strategy for automated trading.
- **Order Execution:** Places market orders using the broker API.
- **Risk Management:** Supports stop-loss, take-profit, and position sizing.
- **Logging & Monitoring:** Logs events, orders, and market data.

---

# **Project Structure**
```
trading_bot/
│
├── config/
│   └── config.py               # Configuration settings (API keys, DB config)
│
├── data/
│   ├── data_fetcher.py         # Market data fetching logic
│   └── historical_data.csv     # Local data storage (if needed)
│
├── strategies/
│   ├── base_strategy.py        # Abstract base class for strategies
│   └── moving_average.py       # Example trading strategy implementation
│
├── models/
│   └── portfolio.py            # Portfolio management logic
│
├── risk/
│   └── risk_manager.py         # Risk management (stop-loss, take-profit)
│
├── brokers/
│   └── broker_api.py           # API wrapper for brokers/exchanges
│
├── utils/
│   ├── logger.py               # Custom logging configuration
│   └── indicators.py           # Custom indicators (RSI, Bollinger Bands)
│
├── main.py                     # Main entry point
├── requirements.txt            # Dependencies
├── README.md                   # Project description
└── .env                        # Secret environment variables (API keys)
```

---

# **Module Breakdown**

### **1. `config/config.py` (Configuration Management)**
Manages API keys, broker URLs, and trading pairs.

```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# IBKR Connection Details
API_KEY = os.getenv("API_KEY", "your_api_key_here")
IBKR_HOST = "127.0.0.1"  # Local TWS or IB Gateway
IBKR_PORT = 7497         # Default port for Paper Trading (7496 for Live)
CLIENT_ID = 1            # Unique client ID (change if needed)

# Trading Bot Settings
START_BALANCE = 10000
TRADING_PAIR = "BTC/USD"

# Debug Print (remove later)
print(f"API_KEY={API_KEY}, IBKR_HOST={IBKR_HOST}, IBKR_PORT={IBKR_PORT}, START_BALANCE={START_BALANCE}")

```

---

### **2. `data/data_fetcher.py` (Market Data Fetching)**
Connects to IBKR API and fetches live market data.

```python
from ib_insync import IB, Stock
import pandas as pd

class DataFetcher:
   def __init__(self, ibkr_host="127.0.0.1", ibkr_port=7497, client_id=1):
      self.ib = IB()
      try:
         print(f"Connecting to {ibkr_host}:{ibkr_port} with clientId {client_id}...")
         self.ib.connect(ibkr_host, ibkr_port, clientId=client_id)
         print("Connection successful!")
      except Exception as e:
         print(f"API connection failed: {e}")
         raise

   def fetch_live_data(self, symbol="AAPL"):
      # Correct way to define a stock contract
      contract = Stock(symbol, "SMART", "USD")
      self.ib.qualifyContracts(contract)

      # Request market data
      market_data = self.ib.reqMktData(contract, "", False, False)
      self.ib.sleep(2)

      # Ensure valid market data is returned
      if market_data.last:
         return pd.DataFrame(
            [{
               "symbol": symbol,
               "price": market_data.last,
               "bid": market_data.bid,
               "ask": market_data.ask,
               "time": market_data.time
            }]
         )
      else:
         raise Exception("Market data not available")

```

---

### **3. `strategies/moving_average.py` (Trading Strategy)**
Implements a simple moving average trading strategy.

```python
import pandas as pd
from strategies.base_strategy import BaseStrategy

class MovingAverageStrategy(BaseStrategy):
   def __init__(self, short_window=5, long_window=20):
      self.short_window = short_window
      self.long_window = long_window

   def generate_signals(self, data: pd.DataFrame):
      data['SMA_Short'] = data['close'].rolling(window=self.short_window).mean()
      data['SMA_Long'] = data['close'].rolling(window=self.long_window).mean()

      # Ensure conversion is done using Pandas DataFrame structure
      data['Signal'] = pd.Series(data['SMA_Short'] > data['SMA_Long'], index=data.index).astype(int)

      return data

```

---

### **4. `models/portfolio.py` (Portfolio Management)**
Handles portfolio balances, holdings, and trade updates.

```python
class Portfolio:
   def __init__(self, initial_balance):
      self.balance = initial_balance
      self.positions = {}  # Dictionary to track holdings

   def update_position(self, symbol, amount, price, action):
      if action == "BUY":
         cost = amount * price
         if cost <= self.balance:
            self.positions[symbol] = self.positions.get(symbol, 0) + amount
            self.balance -= cost
         else:
            raise ValueError("Not enough balance to buy")
      elif action == "SELL":
         if symbol in self.positions and self.positions[symbol] >= amount:
            self.positions[symbol] -= amount
            self.balance += amount * price
         else:
            raise ValueError("Not enough holdings to sell")
      else:
         raise ValueError("Invalid action specified")

```

---

### **5. `brokers/broker_api.py` (Order Placement)**
Manages order placement using IBKR API.

```python
from ib_insync import Stock, MarketOrder

class BrokerAPI:
    def __init__(self, ibkr_host="127.0.0.1", ibkr_port=7497, client_id=1):
        self.ib = IB()
        self.ib.connect(ibkr_host, ibkr_port, clientId=client_id)

    def place_order(self, symbol, side, quantity):
        contract = Stock(symbol, "SMART", "USD")
        order = MarketOrder(side, quantity)
        trade = self.ib.placeOrder(contract, order)
        if trade.orderStatus.status == "Filled":
            return trade
        else:
            raise Exception("Order placement failed")
```

---

### **6. `main.py` (Application Entry Point)**
Runs the bot, fetches market data, and places simulated trades.

```python
from config.config import IBKR_HOST, IBKR_PORT, CLIENT_ID, START_BALANCE
from data.data_fetcher import DataFetcher
from utils.logger import setup_logger

logger = setup_logger()

def main():
   logger.info("Starting trading bot...")

   # Initialize DataFetcher with correct host and port
   try:
      data_fetcher = DataFetcher(IBKR_HOST, IBKR_PORT, CLIENT_ID)
      market_data = data_fetcher.fetch_live_data("AAPL")
      logger.info(f"Market data fetched: {market_data}")
   except Exception as e:
      logger.error(f"Failed to start trading bot: {e}")

if __name__ == "__main__":
   main()

```

---

### **7. `risk/risk_manager.py` (Risk Management)**
Manages risk by applying stop-loss, take-profit, and position sizing strategies.

```python
class RiskManager:
    def __init__(self, stop_loss_percent=0.05, take_profit_percent=0.1):
        self.stop_loss_percent = stop_loss_percent
        self.take_profit_percent = take_profit_percent

    def evaluate_risk(self, entry_price, current_price):
        stop_loss_price = entry_price * (1 - self.stop_loss_percent)
        take_profit_price = entry_price * (1 + self.take_profit_percent)

        if current_price <= stop_loss_price:
            return "STOP_LOSS"
        elif current_price >= take_profit_price:
            return "TAKE_PROFIT"
        else:
            return "HOLD"
```

---

### **8. `utils/indicators.py` (Custom Indicators)**
Implements trading indicators such as RSI and Bollinger Bands.

```python
import pandas as pd

class Indicators:
    @staticmethod
    def calculate_rsi(data, window=14):
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    @staticmethod
    def calculate_bollinger_bands(data, window=20, num_std_dev=2):
        rolling_mean = data['close'].rolling(window=window).mean()
        rolling_std = data['close'].rolling(window=window).std()
        upper_band = rolling_mean + (rolling_std * num_std_dev)
        lower_band = rolling_mean - (rolling_std * num_std_dev)
        return rolling_mean, upper_band, lower_band
```

---

### **How to Run the Project**

1. **Delete Old Virtual Environments:**
   ```bash
   rm -rf .venv venv
   ```

2. **Create a Virtual Environment:**
   ```bash
   python3 -m venv .venv
   ```

3. **Activate the Virtual Environment:**
   ```bash
   source .venv/bin/activate
   ```

4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Bot:**
   ```bash
   python main.py
   ```

