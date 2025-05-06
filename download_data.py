import yfinance as yf

def download_data(symbol, start_date="2022-01-01", end_date="2025-04-23"):
    df = yf.download(symbol, start=start_date, end=end_date)
    df.reset_index(inplace=True)
    df.rename(columns={"Date": "timestamp"}, inplace=True)
    df.to_csv(f"data/{symbol}.csv", index=False)
    print(f"Saved to data/{symbol}.csv")

if __name__ == "__main__":
    download_data("AAPL")  # You can change to MSFT, TSLA, etc.
