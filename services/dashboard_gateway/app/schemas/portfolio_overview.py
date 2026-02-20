from pydantic import BaseModel
from datetime import datetime

class PortfolioOverview(BaseModel):
    timestamp: datetime
    total_value: float
    daily_pnl: float
    unrealized_pnl: float
    realized_pnl: float
    cash: float
    exposure_by_symbol: dict[str, float]
    exposure_by_strategy: dict[str, float]

