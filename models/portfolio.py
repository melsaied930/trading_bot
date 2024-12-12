class Portfolio:
    def __init__(self, initial_balance):
        self.balance = initial_balance
        self.positions = {}
        self.commissions = 0.0

    def update_position(self, symbol, amount, price, action, commission):
        if action == "BUY":
            cost = amount * price + commission
            if cost <= self.balance:
                self.positions[symbol] = self.positions.get(symbol, 0) + amount
                self.balance -= cost
                self.commissions += commission
            else:
                raise ValueError("Not enough balance to buy")
        elif action == "SELL":
            if symbol in self.positions and self.positions[symbol] >= amount:
                self.positions[symbol] -= amount
                self.balance += amount * price - commission
                self.commissions += commission
            else:
                raise ValueError("Not enough holdings to sell")
        else:
            raise ValueError("Invalid action specified")