class MovingAverageStrategy:
    def __init__(self):
        self.previous_price = None

    def make_decision(self, price):
        if self.previous_price is None:
            self.previous_price = price
            return None

        if price > self.previous_price:
            self.previous_price = price
            return "BUY"
        elif price < self.previous_price:
            self.previous_price = price
            return "SELL"
        else:
            return "HOLD"
