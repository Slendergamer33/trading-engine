import pandas as pd

class MomentumBreakoutStrategy:
    def __init__(self, short_window=5, long_window=20):
        self.lookback = long_window
        self.prices = []

    def on_new_bar(self, bar):
        price = float(bar['close'])
        self.prices.append(price)

        if len(self.prices) < self.lookback:
            return None

        recent_prices = pd.Series(self.prices[-self.lookback:])
        max_price = recent_prices.max()
        min_price = recent_prices.min()

        if price >= max_price:
            return 'BUY'
        elif price <= min_price:
            return 'SELL'
        else:
            return None
