from collections import deque

class TradingEngine:
    def __init__(self, data_handler, strategy, portfolio, broker):
        self.data_handler = data_handler
        self.strategy = strategy
        self.portfolio = portfolio
        self.broker = broker
        self.historical_prices = deque(maxlen=1000)

    def run(self):
        while True:
            bar = self.data_handler.get_next_bar()
            if bar is None:
                break

            self.historical_prices.append(bar['close'])

            signal = self.strategy.on_new_bar(bar)
            if signal in ['BUY', 'SELL']:
                order_event = {
                    "type": "ORDER",
                    "symbol": "AAPL",  # You can make this dynamic later
                    "price": float(bar['close']),
                    "quantity": 1,
                    "side": signal
                }

                fill = self.broker.execute_order(order_event)
                self.portfolio.update_fill(fill)
