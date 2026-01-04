from datetime import date
from pydantic import BaseModel

class DailyOHLCVResponse(BaseModel):
    symbol: str
    trading_date: date
    open: float
    high: float
    low: float
    close: float
    volume: int | None