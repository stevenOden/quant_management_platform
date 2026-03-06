from sqlmodel import SQLModel, Field
from datetime import datetime

class CurrentPnl(SQLModel, table=True):
    id: int = Field(default=1, primary_key=True)
    timestamp: datetime
    realized_pnl: float
    unrealized_pnl: float
    total_pnl: float
    portfolio_value: float
