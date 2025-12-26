import httpx
import asyncio
from sqlmodel import Session
from app.models.trade import Trade
from fastapi import HTTPException

DATA_SERVICE_URL = "http://localhost:8001/prices"
PORTFOLIO_SERVICE_URL = "http://localhost:8002/portfolio"
async def execute_trade(trade_in, session: Session):
    symbol = trade_in.symbol.upper()

    # 0. If trade is a sell verify that portfolio hold enough to execute
    side = trade_in.side.upper()
    qty = trade_in.quantity
    if side == "SELL":
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{PORTFOLIO_SERVICE_URL}/positions/{symbol}")
            if response.status_code == 404:
                raise HTTPException(status_code = 400, detail="Cannot execute SELL on symbol not held in portfolio")
            curr_qty = response.json()["quantity"]
            if curr_qty < qty:
                raise HTTPException(status_code=400, detail="Cannot execute SELL: trade qty exceeds portfolio qty")


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

    # 3. Commit to DB
    session.add(trade)
    session.commit()
    session.refresh(trade)

    # 4. Notify Portfolio Service
    asyncio.create_task(notify_portfolio(trade))

    return trade

async def notify_portfolio(executed_trade):
    payload = {
        "trade_id": executed_trade.id,
        "symbol": executed_trade.symbol,
        "quantity": executed_trade.quantity,
        "price": executed_trade.price,
        "side": executed_trade.side,
        "timestamp": executed_trade.timestamp.isoformat()
    }
    max_retries = 5
    backoff = 1 # seconds
    async with httpx.AsyncClient() as client:
        for attempt in range(1, max_retries + 1):
            try:
                response = await client.post(
                    f"{PORTFOLIO_SERVICE_URL}/positions/update",
                    json=payload,
                    timeout=10
                )
                response.raise_for_status()
                print(f"Portfolio updated successfully")
                return True
            except Exception as e:
                print(f"Portfolio update failed: {e}, retrying")

                if attempt == max_retries:
                    print("Cannot update Portfolio")
                    return False

                await asyncio.sleep(backoff)
                backoff *=2 # exponential backoff