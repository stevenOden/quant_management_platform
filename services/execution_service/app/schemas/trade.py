from pydantic import BaseModel
from datetime import datetime

class TradeCreate(BaseModel):
    symbol: str
    quantity: float
    side: str # "BUY" or "SELL"

class TradeRead(BaseModel):
    symbol: str
    quantity: float
    price: float
    side: str
    timestamp: datetime
