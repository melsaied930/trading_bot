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
