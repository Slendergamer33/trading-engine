import argparse
import logging
import pandas as pd
import matplotlib.pyplot as plt
from collections import deque
from data.data_feed import HistoricCSVDataHandler
from strategies.sma_crossover import SMACrossoverStrategy
from strategies.bollinger_bands import BollingerBandsStrategy
from strategies.mean_reversion import MeanReversionStrategy
from strategies.rsi_sma import RSIAndSMAStrategy
from strategies.momentum_breakout import MomentumBreakoutStrategy
from portfolio.portfolio import Portfolio
from execution.broker import SimulatedBroker
from utils.performance import calculate_performance_metrics
from utils.report import generate_markdown_report

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

STRATEGY_MAP = {
    "sma": SMACrossoverStrategy,
    "bollinger": BollingerBandsStrategy,
    "meanrev": MeanReversionStrategy,
    "rsi_sma": RSIAndSMAStrategy,
    "momentum": MomentumBreakoutStrategy
}

class TradingEngine:
    def __init__(self, data_handler, strategy, portfolio, broker):
        self.data_handler = data_handler
        self.strategy = strategy
        self.portfolio = portfolio
        self.broker = broker
        self.historical_prices = deque(maxlen=1000)
        self.equity_curve = []
        self.trade_markers = []
        self.price_history = []

    def run(self):
        timestep = 0
        while True:
            bar = self.data_handler.get_next_bar()
            if bar is None:
                break

            try:
                price = float(bar['close'])
            except ValueError:
                logging.warning(f"Skipping row with invalid close price: {bar['close']}")
                continue

            self.historical_prices.append(price)
            self.price_history.append(price)

            signal = self.strategy.on_new_bar(bar)
            if signal in ['BUY', 'SELL']:
                order_event = {
                    "type": "ORDER",
                    "symbol": "AAPL",  # Make dynamic later
                    "price": price,
                    "quantity": 1,
                    "side": signal
                }

                fill = self.broker.execute_order(order_event)
                self.portfolio.update_fill(fill)
                self.trade_markers.append((timestep, price, signal))

            self.equity_curve.append(self.portfolio.cash)
            timestep += 1

        logging.info(f"Final cash: {self.portfolio.cash}")
        logging.info(f"Positions: {self.portfolio.positions}")
        logging.info(f"Trades: {len(self.broker.order_history)}")

        # Save results
        results_df = pd.DataFrame({"equity": self.equity_curve})
        results_df.to_csv("results/equity_curve.csv", index=False)

        # Calculate performance metrics
        metrics = calculate_performance_metrics(self.equity_curve)
        logging.info(f"Performance Metrics: {metrics}")

        # Plot price + trades
        plt.figure(figsize=(14, 6))
        plt.plot(self.price_history, label="Price", linewidth=1.5, color='black', alpha=0.6)
        for idx, price, action in self.trade_markers:
            color = 'green' if action == 'BUY' else 'red'
            marker = '^' if action == 'BUY' else 'v'
            plt.scatter(idx, price, color=color, label=action if idx == self.trade_markers[0][0] else "", marker=marker)
        plt.title("Price Chart with Trade Signals")
        plt.xlabel("Time Step")
        plt.ylabel("Price")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("results/price_signals_plot.png")
        plt.show()

        # Generate Markdown report
        generate_markdown_report(metrics, len(self.broker.order_history), self.strategy.__class__.__name__)

def parse_args():
    parser = argparse.ArgumentParser(description="Run a backtest on historical data.")
    parser.add_argument("--symbol", type=str, default="AAPL", help="Symbol")
    parser.add_argument("--cash", type=float, default=100000.0, help="Initial cash")
    parser.add_argument("--data", type=str, default="data/AAPL.csv", help="Path to CSV data file")
    parser.add_argument("--short", type=int, default=5, help="Short SMA window")
    parser.add_argument("--long", type=int, default=20, help="Long SMA window")
    parser.add_argument("--strategy", type=str, default="sma", choices=STRATEGY_MAP.keys(), help="Strategy to use")
    return parser.parse_args()

def main():
    args = parse_args()
    data_handler = HistoricCSVDataHandler(args.data)
    strategy_class = STRATEGY_MAP[args.strategy]
    strategy = strategy_class(short_window=args.short, long_window=args.long)
    portfolio = Portfolio(initial_cash=args.cash)
    broker = SimulatedBroker()

    engine = TradingEngine(data_handler, strategy, portfolio, broker)
    engine.run()

if __name__ == "__main__":
    main()