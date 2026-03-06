from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime
from datetime import datetime
from zoneinfo import ZoneInfo
from sqlalchemy.dialects.postgresql import TIMESTAMP

from app.utility import get_time_eastern_timezone
eastern_time_zone = ZoneInfo("America/New_York")

class IntradayPnl(SQLModel, table=True):
    timestamp: datetime = Field(primary_key=True)
    realized_pnl: float
    unrealized_pnl: float
    total_pnl: float
    portfolio_value: float
