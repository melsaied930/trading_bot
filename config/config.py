import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# IBKR Connection Details
API_KEY = os.getenv("API_KEY")
IBKR_HOST = os.getenv("IBKR_HOST", "127.0.0.1")
IBKR_PORT = int(os.getenv("IBKR_PORT", 7497))
CLIENT_ID = int(os.getenv("CLIENT_ID", 1))
START_BALANCE = float(os.getenv("START_BALANCE", 10000))

# Validate environment variables
if not API_KEY:
    raise ValueError("API_KEY is not set in .env file")
