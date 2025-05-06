import pandas as pd

class MeanReversionStrategy:
    def __init__(self, short_window=5, long_window=20):
        self.window = long_window
        self.prices = []

    def on_new_bar(self, bar):
        price = float(bar['close'])
        self.prices.append(price)

        if len(self.prices) < self.window:
            return None

        mean_price = pd.Series(self.prices[-self.window:]).mean()
        if price < mean_price * 0.98:
            return 'BUY'
        elif price > mean_price * 1.02:
            return 'SELL'
        else:
            return None
