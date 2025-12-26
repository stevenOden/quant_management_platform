from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db import get_session
from app.schemas.trade import TradeCreate, TradeRead
from app.services.execution_service import execute_trade

router = APIRouter(prefix="/execute", tags=["Execution"])

@router.post("/", response_model=TradeRead)
async def execute_order(trade: TradeCreate, session: Session = Depends(get_session)):
    return await execute_trade(trade, session)