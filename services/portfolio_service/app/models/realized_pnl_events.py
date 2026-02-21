from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class RealizedPnlEvents(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime
    symbol: str
    quantity: float
    execution_price: float
    pnl_before: float
    pnl_delta: float
    pnl_after: float
    trade_id: str