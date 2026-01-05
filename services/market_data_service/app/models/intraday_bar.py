from datetime import datetime
from pydantic import BaseModel

class IntradayBar(BaseModel):
    symbol: str
    timestamp: datetime
    granularity: str  # e.g. "1m"
    open: float
    high: float
    low: float
    close: float
    volume: int
