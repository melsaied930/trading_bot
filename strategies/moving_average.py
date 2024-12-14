import time

class Strategy:
    def __init__(self, buy_interval=10, sell_delay=5):
        self.last_buy_time = 0
        self.buy_interval = buy_interval  # Buy every 10 seconds
        self.sell_delay = sell_delay  # Sell after 5 seconds
        self.holding_position = False

    def make_decision(self):
        current_time = time.time()

        # Buy Logic: Every 10 seconds
        if not self.holding_position and (current_time - self.last_buy_time >= self.buy_interval):
            self.last_buy_time = current_time
            self.holding_position = True
            print("Decision: BUY+")
            return "BUY"

        # Sell Logic: Sell 5 seconds after the last buy
        if self.holding_position and (current_time - self.last_buy_time >= self.sell_delay):
            self.holding_position = False
            print("Decision: SELL-")
            return "SELL"

        print("Decision: HOLD=")
        return "HOLD"
