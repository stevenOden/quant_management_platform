from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class LatestPrice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str
    price: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class PriceHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str
    price: float
    timestamp:datetime = Field(default_factory=datetime.utcnow)