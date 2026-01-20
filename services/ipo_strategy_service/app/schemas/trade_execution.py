from datetime import datetime
from pydantic import BaseModel

class Trade(BaseModel):
    trade_id: int
    symbol: str
    quantity: float
    price: float
    side: str # "BUY" or "SELL"
    timestamp: datetime