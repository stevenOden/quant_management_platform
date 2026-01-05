from sqlmodel import Session, select
from app.models.intraday_watchlist import IntradayWatchlist
from datetime import datetime, timezone

def add_intraday_symbol(session: Session, symbol: str, source: str | None = None) -> IntradayWatchlist:
    '''Insert a symbol into SymbolUniverse if it doesn't already exist'''

    normalized = symbol.strip().upper()

    existing = session.exec(
        select(IntradayWatchlist).where(IntradayWatchlist.symbol == normalized,IntradayWatchlist.source == source)
    ).one_or_none()

    if existing:
        return existing

    new_row = IntradayWatchlist(
        symbol=normalized,
        source=source
    )

    session.add(new_row)
    session.commit()
    session.refresh(new_row)
    return new_row

def remove_intraday_symbol(session: Session, symbol: str, source: str) -> IntradayWatchlist | None:
    '''Remove Row from Table for a particular symbol and Strategy/Service when no longer in use'''
    normalized = symbol.strip().upper()
    row = session.exec(
        select(IntradayWatchlist).where(IntradayWatchlist.symbol == normalized, IntradayWatchlist.source == source)
    ).first()
    if row:
        session.delete(row)
        session.commit()

    return row

def get_intraday_symbols(session: Session) -> list[str]:
    '''Return all symbols in the universe. Can be filtered on only active symbols'''
    rows = session.exec(select(IntradayWatchlist.symbol).distinct())
    symbols = [row[0] for row in rows]

    return symbols