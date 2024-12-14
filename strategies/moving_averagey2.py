import pandas as pd

class EMAStrategy:
    def __init__(self, ema_period=5):
        self.ema_period = ema_period
        self.prices = []

    def calculate_ema(self):
        if len(self.prices) >= self.ema_period:
            price_series = pd.Series(self.prices[-self.ema_period:])
            ema = price_series.ewm(span=self.ema_period, adjust=False).mean().iloc[-1]
            return ema
        return None

    def make_decision(self, price):
        # Store the latest price
        self.prices.append(price)

        # Ensure we have enough data for EMA calculation
        ema = self.calculate_ema()
        if ema is None:
            print("Not enough data to calculate EMA.")
            return None  # No action until EMA can be computed

        # Trading decisions based on EMA
        print(f"Current Price: {price}, EMA 100: {ema}")
        if price > ema:
            print("Decision: BUY")
            return "BUY"
        elif price < ema:
            print("Decision: SELL")
            return "SELL"
        else:
            print("Decision: HOLD")
            return "HOLD"
