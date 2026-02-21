from sqlmodel import SQLModel, Field
from datetime import datetime

class IntradayPnl(SQLModel, table=True):
    timestamp: datetime = Field(primary_key=True)
    realized_pnl: float
    unrealized_pnl: float
    total_pnl: float
    portfolio_value: float
