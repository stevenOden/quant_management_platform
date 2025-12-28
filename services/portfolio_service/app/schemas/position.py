from sqlmodel import SQLModel
from datetime import datetime

class PositionCreate(SQLModel):
    symbol: str
    quantity: float
    average_cost: float

class PositionRead(SQLModel):
    symbol: str
    quantity: float
    average_cost: float

class TradeUpdate(SQLModel):
    symbol: str
    quantity: float
    price: float
    side: str
    timestamp: datetime
    trade_id: int