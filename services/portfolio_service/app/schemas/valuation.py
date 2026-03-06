from sqlmodel import SQLModel
from typing import List
from datetime import datetime, date

class PositionValuation(SQLModel):
    symbol: str
    quantity: float
    average_cost: float
    latest_price: float
    market_value: float
    unrealized_pnl: float

class PortfolioSummary(SQLModel):
    total_market_value:float
    total_unrealized_pnl:float # Should this also track realized pnl
    positions: List[PositionValuation]

class CashBalance(SQLModel):
    amount: float

class PortfolioOverview(SQLModel):
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

class DailyPnl(SQLModel):
    timestamp: datetime
    recorded_value: float
    recorded_pnl: float
    recorded_pnl_percent: float

class DailyValue(SQLModel):
    datestamp: date
    portfolio_value: float

class IntradayValue(SQLModel):
    timestamp: datetime
    portfolio_value: float