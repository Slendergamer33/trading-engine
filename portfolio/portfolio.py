class Portfolio:
    def __init__(self, initial_cash=100000):
        self.cash = initial_cash
        self.positions = {}

    def update_fill(self, fill_event):
        symbol = fill_event["symbol"]
        price = fill_event["price"]
        quantity = fill_event["quantity"]
        side = fill_event["side"]

        if side == "BUY":
            cost = price * quantity
            if self.cash >= cost:
                self.cash -= cost
                self.positions[symbol] = self.positions.get(symbol, 0) + quantity

        elif side == "SELL":
            if self.positions.get(symbol, 0) >= quantity:
                self.cash += price * quantity
                self.positions[symbol] -= quantity
