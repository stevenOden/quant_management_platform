from sqlmodel import SQLModel, create_engine, Session, select
from app.models.price import LatestPrice, PriceHistory
from datetime import datetime

DATABASE_URL = "sqlite:///./prices.db"
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)

def normalize_symbol(symbol: str) -> str:
    return symbol.strip().upper()

def get_latest_price(symbol: str, session):
    symbol = normalize_symbol(symbol)
    statement = select(LatestPrice).where(LatestPrice.symbol == symbol)
    result = session.exec(statement).first()
    return result

def get_price_history(symbol: str, limit: int, session, order: str = "asc"):
    symbol = normalize_symbol(symbol)
    statement = (
        select(PriceHistory)
        .where(PriceHistory.symbol == symbol)
        .order_by(PriceHistory.timestamp.desc())
        .limit(limit)
    )
    results = session.exec(statement).all()
    if order == "asc":
        return list(reversed(results)) # default sort from oldest to newest for plotting
    return results

def save_latest_price(symbol: str, price: float, session):
    """Insert or update the latest price for a symbol."""
    symbol = symbol.upper()

    # 1. Check if a row already exists
    statement = select(LatestPrice).where(LatestPrice.symbol == symbol)
    existing = session.exec(statement).first()

    # 2. If it exists, update it
    if existing:
        existing.price = price
        existing.timestamp=datetime.utcnow()
        session.add(existing) # insert into LatestPrice updated row for symbol


    # 3. If it doesn't exist, insert a new row
    else:
        new_row = LatestPrice(
            symbol=symbol,
            price=price,
            timestamp=datetime.utcnow()
        )
        session.add(new_row) # insert the newly constructed row

def add_price_history(symbol: str, price: float, session):
    """Append a new historical price row"""
    row = PriceHistory(
        symbol=symbol.upper(),
        price=price,
        timstamp=datetime.utcnow()
    )
    session.add(row)