import pandas as pd

class BollingerBandsStrategy:
    def __init__(self, short_window=20, long_window=50):
        self.window = short_window
        self.stddev = 2
        self.prices = []

    def on_new_bar(self, bar):
        price = float(bar['close'])
        self.prices.append(price)

        if len(self.prices) < self.window:
            return None

        series = pd.Series(self.prices[-self.window:])
        sma = series.mean()
        upper = sma + self.stddev * series.std()
        lower = sma - self.stddev * series.std()

        if price > upper:
            return 'SELL'
        elif price < lower:
            return 'BUY'
        else:
            return None
