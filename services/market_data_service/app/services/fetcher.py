from datetime import timezone
import yfinance as yf
from pyarrow import timestamp

from app.models.intraday_bar import IntradayBar

async def fetch_latest_1m_bar(symbol:str) -> IntradayBar | None:
    ticker = yf.Ticker(symbol)
    df = ticker.history("2m", interval="1m")
    if df.empty:
        return None

    last = df.iloc[-1]
    timestamp = last.name.to_pydatetime().astimezone(timezone.utc)

    return IntradayBar(
        symbol=symbol,
        timestamp=timestamp,
        granularity="1m",
        open=float(last["Open"]),
        high=float(last["High"]),
        low=float(last["Low"]),
        close=float(last["Close"]),
        volume=float(last["Volume"] or 0)
    )