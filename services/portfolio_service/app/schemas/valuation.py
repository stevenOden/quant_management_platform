from sqlmodel import SQLModel
from typing import List

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