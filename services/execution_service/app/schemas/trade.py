from pydantic import BaseModel
from datetime import datetime

class TradeCreate(BaseModel):
    symbol: str
    quantity: float
    side: str # "BUY" or "SELL"

class TradeRead(BaseModel):
    trade_id: int
    symbol: str
    quantity: float
    price: float
    side: str
    timestamp: datetime
