# /Users/mohamed/IdeaProjects/trading_bot/brokers/broker_api.py

from ib_insync import IB, Stock, MarketOrder
import time
import random

class BrokerAPI:
    def __init__(self, ibkr_host="127.0.0.1", ibkr_port=7497):
        self.ib = IB()
        connected = False

        while not connected:
            client_id = self.generate_client_id()
            print(f"Attempting to connect with clientId: {client_id}")

            try:
                if self.ib.connect(ibkr_host, ibkr_port, clientId=client_id, timeout=60):
                    print(f"Connected successfully with clientId: {client_id}")
                    connected = True
                else:
                    raise ConnectionError("IBKR API connection failed.")
            except Exception as e:
                print(f"Connection failed with clientId {client_id}: {e}")
                time.sleep(2)  # Wait before retrying

    @staticmethod
    def generate_client_id():
        """Generate a unique clientId using timestamp and random number."""
        timestamp = int(time.time() % 100000)
        random_suffix = random.randint(1000, 9999)
        return timestamp + random_suffix

    def place_order(self, symbol, side, quantity, order_ref):
        if not self.ib.isConnected():
            raise ConnectionError("Not connected to IBKR API.")

        # Define Stock Contract
        contract = Stock(symbol, "SMART", "USD")
        self.ib.qualifyContracts(contract)

        # Create Market Order
        order_type = "BUY" if side == "BUY" else "SELL"
        order = MarketOrder(order_type, quantity)
        order.orderRef = order_ref

        # Submit Order
        try:
            trade = self.ib.placeOrder(contract, order)
            self.ib.sleep(2)

            # Check if the order is successfully filled
            if trade.orderStatus.status == "Filled":
                print(f"Order Filled: {order_type} {quantity} of {symbol} at {trade.orderStatus.avgFillPrice}")
                return trade
            else:
                print(f"Order Submission Failed: {trade.orderStatus}")
                return None
        except Exception as e:
            print(f"Order Placement Error: {e}")
            raise
