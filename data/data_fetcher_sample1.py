from ib_insync import IB, Stock
import pandas as pd


def stream_market_data(symbol="AAPL", host="127.0.0.1", port=7497, client_id=1):
    ib = IB()
    last_data = None

    try:
        # Connect to the IBKR gateway
        ib.connect(host, port, clientId=client_id)
        print(f"Connected to IBKR at {host}:{port}")

        # Define the stock contract
        contract = Stock(symbol, "SMART", "USD")
        ib.qualifyContracts(contract)

        # Request live streaming market data
        market_data = ib.reqMktData(contract, "", False, False)

        # Define an update handler
        def on_market_data_update(md):
            nonlocal last_data
            current_data = (
                round(md.last, 2) if md.last else None,
                round(md.bid, 2) if md.bid else None,
                round(md.ask, 2) if md.ask else None
            )
            if current_data != last_data and all(value is not None for value in current_data):
                last_data = current_data
                data = [
                    f"Symbol: {symbol}",
                    f"Price: {current_data[0]:.2f}",
                    f"Bid: {current_data[1]:.2f}",
                    f"Ask: {current_data[2]:.2f}",
                    f"Time: {md.time or 'N/A'}"
                ]
                print(" | ".join(data))

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