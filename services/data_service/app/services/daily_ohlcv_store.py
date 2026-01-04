from datetime import date
from sqlmodel import Session, select
from app.models.daily_ohlcv import DailyOHLCV
from app.services.data_store import normalize_symbol


def get_daily_ohlcv_for_symbol(symbol: str, day: date, session: Session) -> DailyOHLCV:
    symbol = normalize_symbol(symbol)
    return session.exec(select(DailyOHLCV).where(DailyOHLCV.symbol == symbol).where(DailyOHLCV.trading_date == day)).first()

def get_all_daily_ohlcv_for_symbol(symbol: str, session: Session) -> DailyOHLCV:
    symbol = normalize_symbol(symbol)
    return session.exec(select(DailyOHLCV).where(DailyOHLCV.symbol == symbol).order_by(DailyOHLCV.trading_date.asc())).all()

def upsert_daily_ohlcv(
        session: Session,symbol: str, day: date, open: float, high: float, low: float, close: float, volume: int | None,
) -> DailyOHLCV:

    existing = get_daily_ohlcv_for_symbol(symbol, day, session)

    if existing:
        existing.open = open
        existing.high = high
        existing.low = low
        existing.close = close
        existing.volume = volume
        session.add(existing)
        return existing

    new_row = DailyOHLCV(
        symbol=symbol,
        trading_date=day,
        open=open,
        high=high,
        low=low,
        close=close,
        volume=volume,
    )
    session.add(new_row)
    return new_row
