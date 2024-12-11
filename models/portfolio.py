class Portfolio:
    def __init__(self, initial_balance):
        self.balance = initial_balance
        self.positions = {}  # Dictionary to track holdings

    def update_position(self, symbol, amount, price, action):
        if action == "BUY":
            cost = amount * price
            if cost <= self.balance:
                self.positions[symbol] = self.positions.get(symbol, 0) + amount
                self.balance -= cost
            else:
                raise ValueError("Not enough balance to buy")
        elif action == "SELL":
            if symbol in self.positions and self.positions[symbol] >= amount:
                self.positions[symbol] -= amount
                self.balance += amount * price
            else:
                raise ValueError("Not enough holdings to sell")
        else:
            raise ValueError("Invalid action specified")
