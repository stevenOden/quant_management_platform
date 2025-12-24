from fastapi import APIRouter
from app.services.data_store import get_session
from sqlmodel import select
from app.models.price import LatestPrice, PriceHistory
from app.services.data_store import (
    get_latest_price,
    get_price_history,
    save_latest_price,
    add_price_history
)
from app.schemas.price import(
    LatestPriceResponse,
    PriceHistoryItem,
    PriceHistoryResponse
)
from app.services.market_data_fetcher import fetch_latest_price

router = APIRouter()

@router.get("/prices/{symbol}/latest", response_model=LatestPriceResponse)
def read_latest_price(symbol: str):
    with get_session() as session:
        price = get_latest_price(symbol, session)
        if price is None:
            raise HTTPException(status_code=404, detail="Symbol not found")
        return price

@router.get("/prices/{symbol}/history", response_model=PriceHistoryResponse)
def read_price_history(symbol: str, limit: int = 100, order: str = "asc"):
    with get_session() as session:
        history = get_price_history(symbol, limit, session, order=order)
        return history

@router.post("/prices/{symbol}/fetch")
def fetch_and_store_price(symbol: str):
    price = fetch_latest_price(symbol)

    if price is None:
        raise HTTPException(status_code = 404, detail="Symbol not found or no data available")
    with get_session() as session:
        save_latest_price(symbol, price, session)
        add_price_history(symbol, price, session)
        session.commit()

    return {
        "symbol": symbol.upper(),
        "price": price,
        "status": "stored"
    }

@router.post("/prices/{symbol}/test-insert")
def test_insert(symbol: str, price: float):
    with get_session() as session:
        save_latest_price(symbol, price, session) # update or insert new price data
        add_price_history(symbol, price, session) # append price data to history
        session.commit()
    return {"status": "ok", "symbol": symbol.upper(), "price":price}
