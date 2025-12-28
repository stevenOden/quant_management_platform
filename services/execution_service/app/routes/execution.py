from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.db import get_session
from app.schemas.trade import TradeCreate, TradeRead
from app.services.execution_service import execute_trade
from app.models.trade import Trade

router = APIRouter(prefix="/execute", tags=["Execution"])

@router.post("/", response_model=TradeRead)
async def execute_order(trade: TradeCreate, session: Session = Depends(get_session)):
    return await execute_trade(trade, session)

@router.get("/trades/all", response_model=list[TradeRead])
def get_all_trades(session: Session = Depends(get_session)):
    '''Get all the trades in the Trade table ordered by execution time.
    Useful for rebuilding the portfolio in the case where the portfolio becomes desynchronized
    from the execution service'''
    trades = session.exec(select(Trade).order_by(Trade.timestamp)).all()
    return trades