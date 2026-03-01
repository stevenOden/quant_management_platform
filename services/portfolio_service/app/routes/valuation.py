from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..db import get_session
from app.services.positions_engine import get_cash_balance
from app.services.pnl_engine import get_cumulative_realized_pnl, get_pnl_snapshot, get_daily_pnl_history, \
    get_intraday_pnl_history
from app.models.current_pnl_snapshot import CurrentPnl
from app.schemas.valuation import PortfolioOverview, DailyValue, IntradayValue
import httpx

from ..utility import get_time_eastern_timezone

router = APIRouter(prefix="/valuation", tags =["valuation"])

@router.get("/overview", response_model = PortfolioOverview)
async def get_portolfio_overview(session: Session = Depends(get_session)):
    cash = await get_cash_balance(session)
    pnl_snapshot = await get_pnl_snapshot(session)
    overview = PortfolioOverview(
        timestamp=pnl_snapshot.timestamp,
        total_value=pnl_snapshot.portfolio_value,
        current_pnl=pnl_snapshot.total_pnl,
        pnl_percent=round(pnl_snapshot.total_pnl/1000000*100,2),
        unrealized_pnl=pnl_snapshot.unrealized_pnl,
        unrealized_pnl_percent=round(pnl_snapshot.unrealized_pnl/1000000*100,2),
        realized_pnl=pnl_snapshot.realized_pnl,
        realized_pnl_percent=round(pnl_snapshot.realized_pnl / 1000000 * 100, 2),
        cash=cash,
        exposure_by_symbol= {},
        exposure_by_strategy= {}
    )
    return overview

@router.get("/cash_balance", response_model=float)
async def get_current_cash_balance(session: Session = Depends(get_session)):
    return await get_cash_balance(session)

@router.get("/realized_pnl", response_model=float)
async def get_current_realized_pnl(session: Session = Depends(get_session)):
    return await get_cumulative_realized_pnl(session)

@router.get("/pnl", response_model=CurrentPnl)
async def get_current_pnl_snapshot(session: Session = Depends(get_session)):
    return await get_pnl_snapshot(session)

@router.get("/daily_pnl", response_model=list[DailyValue])
async def get_daily_pnl(session: Session = Depends(get_session)):
    return await get_daily_pnl_history(session)

@router.get("/intraday_pnl", response_model=list[IntradayValue])
async def get_intraday_pnl(session: Session = Depends(get_session)):
    return await get_intraday_pnl_history(session)