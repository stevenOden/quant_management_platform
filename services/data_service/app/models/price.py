from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional

class LatestPrice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str
    price: float
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class PriceHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str
    price: float
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))