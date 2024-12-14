# strategies/backtest_strategy.py

class BacktestStrategy:
    def __init__(self):
        self.last_buy_price = None
        self.trades = []
        self.profit = 0.0

    def make_decision(self, price):
        """Simple Backtest Trading Logic: Buy Low, Sell High"""
        if self.last_buy_price is None:
            print(f"Decision: BUY at {price}")
            self.last_buy_price = price
            return "BUY"

        if price > self.last_buy_price * 1.02:  # Sell if profit exceeds 2%
            print(f"Decision: SELL at {price}")
            return "SELL"

        print("Decision: HOLD")
        return "HOLD"

    def place_order(self, symbol, side, price, timestamp):
        """Simulate placing orders in backtest."""
        if side == "BUY":
            self.last_buy_price = price
        elif side == "SELL" and self.last_buy_price:
            profit = price - self.last_buy_price
            self.profit += profit
            self.trades.append(
                {
                    "timestamp": timestamp,
                    "symbol": symbol,
                    "side": side,
                    "price": price,
                    "profit": profit,
                }
            )
            self.last_buy_price = None
            print(f"Trade executed: {side} {symbol} at {price} | Profit: {profit}")
