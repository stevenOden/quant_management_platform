from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class CashBalanceEvents(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime
    symbol: str
    quantity: float
    execution_price: float
    cash_before: float
    cash_delta: float
    cash_after: float
    trade_id: str