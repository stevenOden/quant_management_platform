from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..db import get_session
from ..models.position import Position
from app.schemas.position import PositionCreate, PositionRead, TradeUpdate
from app.schemas.valuation import CashBalance
from app.services.positions_engine import get_cash_balance
from app.services.pnl_engine import get_cumulative_realized_pnl, get_pnl_snapshot
from app.models.current_pnl_snapshot import CurrentPnl
import httpx

router = APIRouter(prefix="/valuation", tags =["valuation"])

@router.get("/cash_balance", response_model=float)
async def get_current_cash_balance(session: Session = Depends(get_session)):
    return await get_cash_balance(session)

@router.get("/realized_pnl", response_model=float)
async def get_current_realized_pnl(session: Session = Depends(get_session)):
    return await get_cumulative_realized_pnl(session)

@router.get("/pnl", response_model=CurrentPnl)
async def get_current_pnl_snapshot(session: Session = Depends(get_session)):
    return await get_pnl_snapshot(session)