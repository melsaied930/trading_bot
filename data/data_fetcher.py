# from ib_insync import IB, Stock
# import time
#
# class DataFetcher:
#     def __init__(self, ibkr_host="127.0.0.1", ibkr_port=7497, client_id=None):
#         self.ib = IB()
#         if client_id is None:
#             client_id = int(time.time() % 10000)  # Use a dynamic client ID
#         print(f"Connecting with clientId: {client_id}")
#
#         if not self.ib.connect(ibkr_host, ibkr_port, clientId=client_id, timeout=60):
#             raise ConnectionError("IBKR API connection failed.")
#
#     def fetch_live_data(self, symbol="AAPL"):
#         contract = Stock(symbol, "SMART", "USD")
#         self.ib.qualifyContracts(contract)
#
#         market_data = self.ib.reqMktData(contract, "", False, False)
#         self.ib.sleep(1)
#
#         if market_data.close or market_data.last:
#             price = market_data.close or market_data.last
#             return {
#                 "symbol": symbol,
#                 "price": price,
#                 "bid": market_data.bid,
#                 "ask": market_data.ask,
#                 "time": market_data.time
#             }
#         else:
#             raise ValueError(f"No market data available for {symbol}")








import time
import random


class DataFetcher:
    def __init__(self):
        self.last_fetch_time = 0
        self.fetch_interval = 30  # Fetch data every 30 seconds

    def fetch_live_data(self, stock_symbol):
        """Fetch simulated live market data every 30 seconds."""
        current_time = time.time()

        # Check if 30 seconds have passed since the last fetch
        if current_time - self.last_fetch_time >= self.fetch_interval:
            self.last_fetch_time = current_time

            # Simulate fetching data
            last_close = round(random.uniform(150, 180), 2)
            current_open = round(last_close + random.uniform(-2, 2), 2)

            # Log fetched data
            print(f"[DataFetcher] Fetched for {stock_symbol} - Last Close: {last_close}, Current Open: {current_open}")

            return {
                "stock_symbol": stock_symbol,
                "last_close": last_close,
                "current_open": current_open
            }
        else:
            # Indicate that data fetching is not performed yet
            print(f"[DataFetcher] Waiting for next fetch interval...")
            return {}
