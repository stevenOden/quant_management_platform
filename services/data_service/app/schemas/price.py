from datetime import datetime
from sqlmodel import SQLModel

class LatestPriceResponse(SQLModel):
    symbol: str
    price: float | None
    timestamp: datetime | None

class PriceHistoryItem(SQLModel):
    price: float
    timestamp: datetime

class PriceHistoryResponse(SQLModel):
    symbol: str
    count: int
    data:list[PriceHistoryitem]