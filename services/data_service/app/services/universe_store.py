from sqlmodel import Session, select
from app.models.universe import SymbolUniverse
from datetime import datetime, timezone

def add_symbol(session: Session, symbol: str, source: str | None = None) -> SymbolUniverse:
    '''Insert a symbol into SymbolUniverse if it doesn't already exist'''

    normalized = symbol.strip().upper()

    existing = session.exec(
        select(SymbolUniverse).where(SymbolUniverse.symbol == normalized)).one_or_none()

    if existing:
        return existing

    new_row = SymbolUniverse(
        symbol=normalized,
        source=source,
        is_active=True,
        added_at=datetime.now(timezone.utc)
    )

    session.add(new_row)
    session.commit()
    session.refresh(new_row)
    return new_row

def get_symbol(session: Session, symbol: str) -> SymbolUniverse | None:
    '''Fetch symbol from universe'''
    normalized = symbol.strip().upper()
    result = session.exec(select(SymbolUniverse).where(SymbolUniverse.symbol == normalized)).one_or_none()
    return result

def get_all_symbols(session: Session, active_only: bool = True) -> list[SymbolUniverse]:
    '''Return all symbols in the universe. Can be filtered on only active symbols'''
    query = select(SymbolUniverse)

    if active_only:
        query = query.where(SymbolUniverse.is_active == True)

    return list(session.exec(query).all())

def deactivate_symbol(session: Session, symbol: str) -> SymbolUniverse | None:
    '''Soft-delete a symbol by deactivating it (setting is_active to False)'''
    row = get_symbol(session,symbol)
    if not row:
        return None

    row.is_active = False
    session.add(row)
    session.commit()
    session.refresh(row)
    return row