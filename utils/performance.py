import numpy as np
import pandas as pd
from scipy.stats import norm


def calculate_performance_metrics(equity_curve):
    equity = np.array(equity_curve)
    returns = np.diff(equity) / equity[:-1]

    metrics = {}
    metrics["total_return"] = float((equity[-1] - equity[0]) / equity[0])
    metrics["sharpe_ratio"] = float(np.mean(returns) / np.std(returns)) * np.sqrt(252) if np.std(returns) > 0 else 0
    metrics["max_drawdown"] = float(max_drawdown(equity))
    metrics["final_equity"] = float(equity[-1])

    return metrics


def max_drawdown(equity):
    roll_max = np.maximum.accumulate(equity)
    drawdown = equity / roll_max - 1.0
    return drawdown.min()
