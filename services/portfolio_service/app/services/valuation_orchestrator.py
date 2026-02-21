import asyncio
from datetime import datetime
from sqlmodel import Session
from app.db import engine

from fastapi import FastAPI
from app.utility import get_time_eastern_timezone
from app.services.positions_engine import get_all_positions, get_cash_balance, get_portfolio_summary
from app.services.pnl_engine import (
    compute_unrealized_pnl,
    get_cumulative_realized_pnl,
    compute_total_pnl,
    compute_portfolio_value,
    write_current_snapshot,
    write_intraday_snapshot_if_needed,
    write_daily_snapshot_if_needed,
)

app = FastAPI()

VALUATION_INTERVAL_SECONDS = 300  # or 60, or 300, etc.
last_daily_update = None

async def valuation_loop():
    with Session(engine) as session:
        while True:
            now = get_time_eastern_timezone()

            # 1. Get current cash balance
            cash = await get_cash_balance(session)

            # 2. Get current portfolio value and unrealized pnl
            portfolio_summary = await get_portfolio_summary(session)
            unrealized_pnl = portfolio_summary.total_unrealized_pnl
            positions_value = portfolio_summary.total_market_value

            # 3. Get realized pnl from Exectuion service
            realized_pnl = await get_cumulative_realized_pnl(session)

            total_pnl = realized_pnl + unrealized_pnl
            portfolio_value = cash + positions_value

            # 4. Write snapshots
            await write_current_snapshot(session, now, realized_pnl, unrealized_pnl, total_pnl, portfolio_value)
            await write_intraday_snapshot_if_needed(session, now, realized_pnl, unrealized_pnl, total_pnl, portfolio_value)
            if not last_daily_update or last_daily_update != now.date():
                await write_daily_snapshot_if_needed(session, now, realized_pnl, unrealized_pnl, total_pnl, portfolio_value)
                last_daily_update = now.date()

            # 5. Sleep until next tick
            await asyncio.sleep(VALUATION_INTERVAL_SECONDS)