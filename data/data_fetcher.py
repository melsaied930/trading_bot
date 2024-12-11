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
