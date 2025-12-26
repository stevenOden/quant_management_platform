from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db import get_session
from app.services.data_store import (
    get_latest_price,
    get_price_history,
    save_latest_price,
    add_price_history
)
from app.schemas.price import(
    LatestPriceResponse,
    PriceHistoryItem,
    PriceHistoryResponse,
    PriceIngestResponse
)
from app.services.market_data_fetcher import fetch_latest_price

router = APIRouter(prefix="/prices")

@router.get("/{symbol}/latest", response_model=LatestPriceResponse)
def read_latest_price(symbol: str, session: Session = Depends(get_session)):
    price = get_latest_price(symbol, session)
    if price is None:
        raise HTTPException(status_code=404, detail="Symbol not found")
    return price

@router.get("/{symbol}/history", response_model=PriceHistoryResponse)
def read_price_history(symbol: str, limit: int = 100, order: str = "asc",session: Session = Depends(get_session)):
    history = get_price_history(symbol, limit, session, order=order)
    return PriceHistoryResponse(
        symbol=symbol,
        count=len(history),
        data = [
            PriceHistoryItem(
                price = row.price,
                timestamp = row.timestamp
            )
            for row in history
        ]
    )

@router.post("/{symbol}/fetch", response_model=PriceIngestResponse)
async def fetch_and_store_price(symbol: str, session: Session = Depends(get_session)): # asynch = this function may wait on I/O, don't block thread
    price = fetch_latest_price(symbol)

    if price is None:
        raise HTTPException(status_code = 404, detail="Symbol not found or no data available")
    save_latest_price(symbol, price, session)
    add_price_history(symbol, price, session)
    session.commit()

    return {
        "symbol": symbol.upper(),
        "price": price,
        "status": "stored"
    }

@router.post("/prices/{symbol}/test-insert")
def test_insert(symbol: str, price: float, session: Session = Depends(get_session)):
    save_latest_price(symbol, price, session) # update or insert new price data
    add_price_history(symbol, price, session) # append price data to history
    session.commit()
    return {"status": "ok", "symbol": symbol.upper(), "price":price}
