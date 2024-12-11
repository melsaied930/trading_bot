from ib_insync import IB, Stock, MarketOrder

class BrokerAPI:
    def __init__(self, ibkr_host="127.0.0.1", ibkr_port=7497, client_id=1):
        self.ib = IB()
        self.ib.connect(ibkr_host, ibkr_port, clientId=client_id)

    def place_order(self, symbol, side, quantity, price):
        contract = Stock(symbol, "SMART", "USD")
        order = MarketOrder("BUY" if side == "BUY" else "SELL", quantity)
        trade = self.ib.placeOrder(contract, order)

        if trade.orderStatus.status == "Filled":
            return trade
        else:
            raise Exception("Order placement failed")
