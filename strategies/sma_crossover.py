import pandas as pd

class SMACrossoverStrategy:
    def __init__(self, short_window=5, long_window=20):
        self.short_window = short_window
        self.long_window = long_window
        self.prices = []

    def on_new_bar(self, bar):
        try:
            price = float(bar['close'])  # Convert to float just in case
        except ValueError:
            print(f"Warning: could not convert price '{bar['close']}' to float")
            return None  # make sure we return early on error

        self.prices.append(price)

        if len(self.prices) < self.long_window:
            return None  # Not enough data yet

        short_sma = pd.Series(self.prices[-self.short_window:]).mean()
        long_sma = pd.Series(self.prices[-self.long_window:]).mean()

        if short_sma > long_sma:
            return 'BUY'
        elif short_sma < long_sma:
            return 'SELL'
        else:
            return None
