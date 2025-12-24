import yfinance as yf
from datetime import datetime

def fetch_latest_price(symbol: str) -> float:
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d")
    if data.empty:
        return None

    # Get the last closing price
    return float(data["Close"].iloc[-1])