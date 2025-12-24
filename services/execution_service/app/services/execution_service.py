import httpx
from sqlmodel import Session
from app.models.trade import Trade

DATA_SERVICE_URL = "http://localhost:8001/prices"
async def execute_trade(trade_in, session: Session):
    symbol = trade_in.symbol.upper()

    # 1. Fetch latest price from data_service
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DATA_SERVICE_URL}/{symbol}/latest")
        latest_price = response.json()["price"]

    # 2. Create trade record
    trade = Trade(
        symbol=symbol,
        quantity=trade_in.quantity,
        price=latest_price, # assume execution price = current price for now - will update with order fill details later
        side=trade_in.side.upper(),
    )

    session.add(trade)
    session.commit()
    session.refresh(trade)

    return trade