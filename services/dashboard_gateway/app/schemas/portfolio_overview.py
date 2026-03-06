from pydantic import BaseModel
from datetime import datetime

class PortfolioOverview(BaseModel):
    timestamp: datetime
    total_value: float
    current_pnl: float
    pnl_percent: float
    unrealized_pnl: float
    unrealized_pnl_percent: float
    realized_pnl: float
    realized_pnl_percent: float
    cash: float
    exposure_by_symbol: dict[str, float]
    exposure_by_strategy: dict[str, float]

