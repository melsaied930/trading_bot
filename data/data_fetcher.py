from ib_insync import IB, Stock
import time

class DataFetcher:
    def __init__(self, ibkr_host="127.0.0.1", ibkr_port=7497, client_id=None):
        self.ib = IB()
        if client_id is None:
            client_id = int(time.time() % 10000)  # Use a dynamic client ID
        print(f"Connecting with clientId: {client_id}")

        if not self.ib.connect(ibkr_host, ibkr_port, clientId=client_id, timeout=60):
            raise ConnectionError("IBKR API connection failed.")

    def fetch_live_data(self, symbol="AAPL"):
        contract = Stock(symbol, "SMART", "USD")
        self.ib.qualifyContracts(contract)

        market_data = self.ib.reqMktData(contract, "", False, False)
        self.ib.sleep(1)

        if market_data.close or market_data.last:
            price = market_data.close or market_data.last
            return {
                "symbol": symbol,
                "price": price,
                "bid": market_data.bid,
                "ask": market_data.ask,
                "time": market_data.time
            }
        else:
            raise ValueError(f"No market data available for {symbol}")
