from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db import get_session
from app.models.intraday_watchlist import IntradayWatchlist
from app.schemas.intraday_watchlist import IntradayWatchlistRequest
from app.services.intraday_watchlist_store import (
    add_intraday_symbol,
    remove_intraday_symbol,
    get_intraday_symbols,
)

router = APIRouter(prefix="/intraday_watchlist")

@router.post("/symbols/add", response_model=IntradayWatchlist)
def register_symbol(payload: IntradayWatchlistRequest, session: Session = Depends(get_session)):
    '''Register a symbol in the universe. Idempotent: returns existing row if exists'''
    return add_intraday_symbol(session, payload.symbol, payload.source)

@router.get("/symbols", response_model=list[str])
def list_symbols(session: Session = Depends(get_session)):
    '''List all symbols in universe. Optionally filters on active only, default is true'''
    return get_intraday_symbols(session)

@router.delete("/symbols/remove", response_model=IntradayWatchlist)
def deactivate_symbol_route(symbol: str, source: str, session: Session = Depends(get_session)):
    '''Soft delete a symbol by marking is_active False'''
    row = remove_intraday_symbol(session, symbol, source)
    if not row:
        raise HTTPException(status_code=500, detail=f"{symbol} from {source} row not found")

    return row