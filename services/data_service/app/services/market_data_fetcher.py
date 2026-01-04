import yfinance as yf
from datetime import date, timedelta

def fetch_latest_price(symbol: str) -> float:
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d")
    if data.empty:
        return None

    # Get the last closing price
    return float(data["Close"].iloc[-1])

def fetch_ohlcv_for_date(symbol: str, day: date) -> dict | None:
    ticker = yf.Ticker(symbol)
    # yfinance requires end = day + 1 to include the day
    start = day
    end = day + timedelta(days=1)

    df = ticker.history(interval="1d", start=start, end=end)

    if df.empty:
        return None

    row = df.iloc[0]

    return {
        "open": float(row["Open"]),
        "high": float(row["High"]),
        "low": float(row["Low"]),
        "close": float(row["Close"]),
        "volume": int(row["Volume"]),
    }
