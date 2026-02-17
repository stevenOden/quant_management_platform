from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db import get_session
from app.models.universe import SymbolUniverse
from app.schemas.universe import SymbolRequest
from app.services.universe_store import (
    add_symbol,
    get_all_symbols,
    deactivate_symbol,
    get_symbol_strategy,
    get_distinct_symbols
)

router = APIRouter(prefix="/universe")

@router.post("/symbols", response_model=SymbolUniverse)
def register_symbol(payload: SymbolRequest, session: Session = Depends(get_session)):
    '''Register a symbol in the universe. Idempotent: returns existing row if exists'''
    return add_symbol(session, payload.symbol, payload.source)

@router.get("/symbols/data", response_model=list[SymbolUniverse])
def list_symbol_data(active_only: bool = True, session: Session = Depends(get_session)):
    '''List all symbols in universe. Optionally filters on active only, default is true'''
    return get_all_symbols(session, active_only=active_only)

@router.get("/symbols", response_model=list[str])
def list_symbols(active_only: bool = True, session: Session = Depends(get_session)):
    '''List all symbols in universe. Optionally filters on active only, default is true'''
    return get_distinct_symbols(session, active_only=active_only)

@router.get("/symbols/{symbol}", response_model=SymbolUniverse)
def list_symbol(symbol:str, strategy:str, active_only: bool = True, session: Session = Depends(get_session)):
    '''List all symbols in universe. Optionally filters on active only, default is true'''
    return get_symbol_strategy(session, symbol, strategy,  active_only=active_only)

@router.delete("/symbols", response_model=SymbolUniverse)
def deactivate_symbol_route(symbol: str, source: str, session: Session = Depends(get_session)):
    '''Soft delete a symbol by marking is_active False'''
    row = deactivate_symbol(session, symbol, source)
    if not row:
        raise HTTPException(status_code=500, detail=f"{symbol} | {source} row not found")

    return row