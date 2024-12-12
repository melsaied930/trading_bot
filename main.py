from data.data_fetcher import DataFetcher
from brokers.broker_api import BrokerAPI
import time

from strategies.moving_average import TestStrategy

if __name__ == "__main__":
    fetcher = DataFetcher()
    strategy = TestStrategy(buy_interval=10, sell_delay=5)
    broker = BrokerAPI()

    while True:
        try:
            # Fetch live market data
            data = fetcher.fetch_live_data("AAPL")
            print(f"Fetched Data: {data}")

            # Make trading decision
            decision = strategy.make_decision()

            if decision in ["BUY", "SELL"]:
                broker.place_order(data['symbol'], decision, 100, f"Order-{int(time.time())}")
                print(f"Order Executed: {decision} at {data['price']}")

            time.sleep(1)
        except Exception as e:
            print(f"Error: {e}")
