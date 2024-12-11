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
