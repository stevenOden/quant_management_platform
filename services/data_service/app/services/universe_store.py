from sqlmodel import Session, select
from app.models.universe import SymbolUniverse
from app.utility import get_time_eastern_timezone

def add_symbol(session: Session, symbol: str, source: str | None = None) -> SymbolUniverse:
    '''Insert a symbol into SymbolUniverse if it doesn't already exist'''

    normalized = symbol.strip().upper()

    existing = session.exec(
        select(SymbolUniverse).where(SymbolUniverse.symbol == normalized, SymbolUniverse.source == source)).one_or_none()

    if existing:
        if existing.is_active:
            return existing
        else:
            existing.is_active = True
            existing.added_at=get_time_eastern_timezone()
            session.add(existing)
            session.commit()
            session.refresh(existing)
            return existing

    new_row = SymbolUniverse(
        symbol=normalized,
        source=source,
        is_active=True,
        added_at=get_time_eastern_timezone()
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

def get_symbol_strategy(session: Session, symbol: str, source: str, active_only: bool = True) -> SymbolUniverse | None:
    '''Fetch symbol from universe'''
    normalized = symbol.strip().upper()
    result = session.exec(select(SymbolUniverse).where(SymbolUniverse.symbol == normalized, SymbolUniverse.source == source)).one_or_none()
    return result

def get_all_symbols(session: Session, active_only: bool = True) -> list[SymbolUniverse]:
    '''Return all symbols in the universe. Can be filtered on only active symbols'''
    query = select(SymbolUniverse)

    if active_only:
        query = query.where(SymbolUniverse.is_active == True)

    return list(session.exec(query).all())

def get_distinct_symbols(session: Session, active_only: bool = True) -> list[SymbolUniverse]:
    '''Return all symbols in the universe. Can be filtered on only active symbols'''
    query = select(SymbolUniverse.symbol)

    if active_only:
        query = query.where(SymbolUniverse.is_active == True)
    query = query.distinct()
    return list(session.exec(query))

def deactivate_symbol(session: Session, symbol: str, source: str) -> SymbolUniverse | None:
    '''Soft-delete a symbol by deactivating it (setting is_active to False)'''
    row = get_symbol_strategy(session,symbol,source)
    if not row:
        return None

    row.is_active = False
    session.add(row)
    session.commit()
    session.refresh(row)
    return row