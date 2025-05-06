import pandas as pd

class RSIAndSMAStrategy:
    def __init__(self, short_window=14, long_window=50):
        self.sma_window = long_window
        self.rsi_window = short_window
        self.prices = []

    def compute_rsi(self, prices):
        delta = pd.Series(prices).diff()
        gain = (delta.where(delta > 0, 0)).rolling(self.rsi_window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(self.rsi_window).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def on_new_bar(self, bar):
        price = float(bar['close'])
        self.prices.append(price)

        if len(self.prices) < max(self.rsi_window, self.sma_window):
            return None

        rsi = self.compute_rsi(self.prices[-self.rsi_window-1:]).iloc[-1]
        sma = pd.Series(self.prices[-self.sma_window:]).mean()

        if rsi < 30 and price > sma:
            return 'BUY'
        elif rsi > 70 and price < sma:
            return 'SELL'
        else:
            return None
