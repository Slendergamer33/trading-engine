class SimulatedBroker:
    def __init__(self):
        self.order_history = []

    def execute_order(self, order_event):
        fill_event = {
            "type": "FILL",
            "symbol": order_event["symbol"],
            "price": order_event["price"],
            "quantity": order_event["quantity"],
            "side": order_event["side"]
        }
        self.order_history.append(fill_event)
        return fill_event
