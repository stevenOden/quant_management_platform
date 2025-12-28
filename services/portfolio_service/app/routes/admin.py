from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select, delete
import httpx

from app.db import engine
from app.models.position import Position
from app.routes.portfolio import update_position_from_trade
from app.schemas.position import TradeUpdate

router = APIRouter(prefix="/admin", tags =["admin"])

EXECUTION_SERVICE_URL = "http://localhost:8003/execute"

@router.post("/resync")
async def resync_portfolio():
    # 1. Get Trade history from Execution service
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{EXECUTION_SERVICE_URL}/trades/all")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reach Execution Service: {e}")

    if response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail=f"Execution Service return {response.status_code}: {response.text}"
            )

    trades = response.json()

    # 2. Clear current Positions Table
    with Session(engine) as session:
        session.exec(delete(Position))
        session.commit()

        # 3. Replay trades in chronological order and rebuild Positions table
        for trade in trades:
            trade_obj = TradeUpdate(**trade)
            update_position_from_trade(trade_obj, session)

        session.commit()

        # 4. Count rebuilt positions
        positions_count = session.exec(select(Position)).all()

    return {
        "status": "resync complete",
        "positions_rebuilt": len(positions_count),
        "trades_replayed": len(trades)
    }