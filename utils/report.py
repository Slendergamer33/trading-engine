def generate_markdown_report(metrics, trade_count, strategy_name):
    with open("results/report.md", "w") as f:
        f.write(f"# Backtest Report\n\n")
        f.write(f"**Strategy:** {strategy_name}\n\n")
        f.write(f"**Total Trades:** {trade_count}\n\n")
        f.write("## Performance Metrics\n")
        for key, value in metrics.items():
            f.write(f"- **{key.replace('_', ' ').title()}:** {value:.4f}\n")
        f.write("\n---\n")
        f.write("![Equity Curve](equity_curve_plot.png)\n")
        f.write("![Price Chart](price_signals_plot.png)\n")
