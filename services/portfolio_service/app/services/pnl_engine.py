from datetime import datetime, timedelta
from typing import List
from sqlmodel import Session, select, delete
from app.models.realized_pnl import RealizedPnl
from app.models.current_pnl_snapshot import CurrentPnl
from app.models.daily_pnl_history import DailyPnl
from app.models.intraday_pnl_history import IntradayPnl
from app.schemas.valuation import DailyValue, IntradayValue
from fastapi import HTTPException

from app.utility import get_today_eastern_timezone, get_time_eastern_timezone


async def get_cumulative_realized_pnl(session: Session) -> float:
    realized_pnl = session.exec(select(RealizedPnl)).one_or_none()
    if realized_pnl is None:
        realized_pnl = RealizedPnl(id=1, amount=0)
        session.add(realized_pnl)
        session.commit()
    return realized_pnl.amount

async def get_daily_pnl_history(session:Session) -> list[DailyValue]:
    one_year_ago = get_today_eastern_timezone() - timedelta(days=365)
    daily_history = session.exec(select(DailyPnl).where(DailyPnl.datestamp >= one_year_ago).
                                 order_by(DailyPnl.datestamp.asc())
                                 ).all()
    return [DailyValue(datestamp=row.datestamp,portfolio_value=row.portfolio_value) for row in daily_history]

async def get_intraday_pnl_history(session:Session) -> list[IntradayValue]:
    intraday_history = session.exec(select(IntradayPnl).order_by(IntradayPnl.timestamp.asc())).all()
    return [IntradayValue(timestamp=row.timestamp,portfolio_value=row.portfolio_value) for row in intraday_history]

async def write_current_snapshot(session: Session, timestamp: datetime,realized: float,unrealized: float,total: float,portfolio_value: float) -> None:
    snapshot = session.exec(select(CurrentPnl)).one_or_none()
    if not snapshot:
        snapshot = CurrentPnl(
            timestamp= timestamp,
            realized_pnl= realized,
            unrealized_pnl= unrealized,
            total_pnl= total,
            portfolio_value= portfolio_value,
        )
    else:
        snapshot.timestamp = timestamp
        snapshot.realized_pnl = realized
        snapshot.unrealized_pnl = unrealized
        snapshot.total_pnl = total
        snapshot.portfolio_value = portfolio_value
    session.add(snapshot)
    session.commit()

async def get_pnl_snapshot(session):
    pnl_snapshot = session.exec(select(CurrentPnl)).one_or_none()
    if not pnl_snapshot:
        raise HTTPException(status_code=404, detail="Current pnl snapshot does not exist")
    return pnl_snapshot

async def write_daily_snapshot_if_needed(
    session: Session,
    timestamp: datetime,
    realized: float,
    unrealized: float,
    total: float,
    portfolio_value: float,
) -> None:
    snapshot = session.exec(select(DailyPnl).where(DailyPnl.datestamp==timestamp.date())).one_or_none()
    if snapshot:
        snapshot.realized_pnl = realized
        snapshot.unrealized_pnl = unrealized
        snapshot.total_pnl = total
        snapshot.portfolio_value = portfolio_value
    else:
        snapshot = DailyPnl(
            datestamp = timestamp.date(),
            realized_pnl=realized,
            unrealized_pnl=unrealized,
            total_pnl=total,
            portfolio_value=portfolio_value
        )
    session.add(snapshot)
    session.commit()

def floor_to_5m(timestamp: datetime):
    minute = (timestamp.minute // 5) * 5
    return timestamp.replace(minute=minute, second = 0, microsecond=0)

async def write_intraday_snapshot_if_needed(
    session: Session,
    timestamp: datetime,
    realized: float,
    unrealized: float,
    total: float,
    portfolio_value: float,
) -> None:
    timestamp = floor_to_5m(timestamp)
    snapshot = session.exec(select(IntradayPnl).where(IntradayPnl.timestamp==timestamp)).one_or_none()
    if snapshot:
        snapshot.realized_pnl = realized
        snapshot.unrealized_pnl = unrealized
        snapshot.total_pnl = total
        snapshot.portfolio_value = portfolio_value
    else:
        snapshot = IntradayPnl(
            timestamp=timestamp,
            realized_pnl=realized,
            unrealized_pnl=unrealized,
            total_pnl=total,
            portfolio_value=portfolio_value
        )
    session.add(snapshot)

    # Remove data that is over 24 hours old
    hour24_cutoff = get_time_eastern_timezone() - timedelta(hours=24)
    session.exec(delete(IntradayPnl).where(IntradayPnl.timestamp < hour24_cutoff))

    session.commit()