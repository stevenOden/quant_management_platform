import yfinance as yf

from app.models.intraday_bar import IntradayBar

async def fetch_latest_1m_bar(symbol:str) -> IntradayBar | None:
    ticker = yf.Ticker(symbol)
    granularity = "5m"
    df = ticker.history("1d", interval=granularity) # Use 5m for testing purposes
    if df.empty:
        return None

    last = df.iloc[-1] # This is the latest candle
    timestamp = last.name.to_pydatetime().astimezone()

    return IntradayBar(
        symbol=symbol,
        timestamp=timestamp,
        granularity=granularity,
        open=float(last["Open"]),
        high=float(last["High"]),
        low=float(last["Low"]),
        close=float(last["Close"]),
        volume=float(last["Volume"] or 0)
    )