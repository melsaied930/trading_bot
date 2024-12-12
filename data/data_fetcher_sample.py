from ib_insync import IB, Stock
import pandas as pd


def stream_market_data(symbol="AAPL", host="127.0.0.1", port=7497, client_id=1):
    ib = IB()
    try:
        # Connect to the IBKR gateway
        ib.connect(host, port, clientId=client_id)
        print(f"Connected to IBKR at {host}:{port}")

        # Define the stock contract
        contract = Stock(symbol, "SMART", "USD")
        ib.qualifyContracts(contract)

        # Request live streaming market data
        market_data = ib.reqMktData(contract, "", False, True)

        # Define an update handler
        def on_market_data_update(md):
            if md.last or md.bid or md.ask:
                data = {
                    "symbol": symbol,
                    "price": md.last or "N/A",
                    "bid": md.bid or "N/A",
                    "ask": md.ask or "N/A",
                    "time": md.time or "N/A"
                }
                print(pd.DataFrame([data]))
            else:
                print(f"No market data available for {symbol}")

        # Subscribe to market data updates
        market_data.updateEvent += on_market_data_update

        # Keep streaming until user interruption
        print("Streaming market data... Press Ctrl+C to stop.")
        ib.run()

    except Exception as e:
        print(f"Error streaming market data: {e}")

    finally:
        ib.disconnect()
        print(f"Disconnected from IBKR at {host}:{port}")


# Run the sample stream data fetcher
stream_market_data("AAPL")
