class RiskManager:
    def __init__(self, stop_loss_percent=0.05, take_profit_percent=0.1):
        self.stop_loss_percent = stop_loss_percent
        self.take_profit_percent = take_profit_percent

    def evaluate_risk(self, entry_price, current_price):
        stop_loss_price = entry_price * (1 - self.stop_loss_percent)
        take_profit_price = entry_price * (1 + self.take_profit_percent)

        if current_price <= stop_loss_price:
            return "STOP_LOSS"
        elif current_price >= take_profit_price:
            return "TAKE_PROFIT"
        else:
            return "HOLD"