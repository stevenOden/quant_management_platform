from datetime import datetime
from typing import List
from sqlmodel import Session, select
from app.models.realized_pnl import RealizedPnl
from app.models.current_pnl_snapshot import CurrentPnl
from app.models.daily_pnl_history import DailyPnl
from app.models.intraday_pnl_history import IntradayPnl

from .models import Position  # or wherever Position lives

def get_cumulative_realized_pnl(session: Session) -> float:
    realized_pnl = session.exec(select(RealizedPnl)).one_or_none()
    if realized_pnl is None:
        realized_pnl = RealizedPnl(id=1, amount=0)
        session.add(realized_pnl)
        session.commit()
    return realized_pnl.amount

def write_current_snapshot(session: Session, timestamp: datetime,realized: float,unrealized: float,total: float,portfolio_value: float) -> None:
    snapshot = CurrentPnl(
        timestamp= timestamp,
        realized_pnl= realized,
        unrealized_pnl= unrealized,
        total_pnl= total,
        portfolio_value= portfolio_value,
    )
    session.add(snapshot)
    session.commit()

def write_intraday_snapshot_if_needed(
    session: Session,
    timestamp: datetime,
    realized: float,
    unrealized: float,
    total: float,
    portfolio_value: float,
) -> None:
    snapshot = DailyPnl(
        date = timestamp.date(),
        realized_pnl=realized,
        unrealized_pnl=unrealized,
        total_pnl=total,
        portfolio_value=portfolio_value
    )
    session.add(snapshot)
    session.commit()

def write_daily_snapshot_if_needed(
    session: Session,
    timestamp: datetime,
    realized: float,
    unrealized: float,
    total: float,
    portfolio_value: float,
) -> None:
    snapshot = IntradayPnl(
        date=timestamp.date(),
        realized_pnl=realized,
        unrealized_pnl=unrealized,
        total_pnl=total,
        portfolio_value=portfolio_value
    )
    session.add(snapshot)
    session.commit()