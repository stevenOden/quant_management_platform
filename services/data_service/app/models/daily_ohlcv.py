from datetime import date, datetime, timezone
from sqlmodel import SQLModel, Field
from sqlalchemy import UniqueConstraint

class DailyOHLCV(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    symbol: str = Field(index=True)
    trading_date: date = Field(index=True)

    open: float
    high: float
    low: float
    close: float
    volume: int | None = None

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        UniqueConstraint("symbol", "trading_date"),
    )
