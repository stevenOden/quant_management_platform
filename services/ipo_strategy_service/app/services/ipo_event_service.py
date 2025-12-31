from fastapi import HTTPException
from sqlmodel import select, Session
from app.models.ipo_event import IPOEvent

def get_symbol(symbol: str, session: Session) -> IPOEvent:
    normalized = symbol.strip().upper()
    result = session.exec(select(IPOEvent).where(IPOEvent.symbol == normalized)).one_or_none()

    if not result:
        raise HTTPException(status_code=404, detail=f"{symbol} not found in IPOEvent Table")

    return result

def get_all_symbols(session: Session) -> list[IPOEvent]:
    return session.exec(select(IPOEvent)).all()
