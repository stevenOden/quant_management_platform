from pydantic import BaseModel
from datetime import datetime

class TradeHistory(BaseModel):
    timestamp: datetime
    symbol: str
    side: str
    quantity: float
    price: float
    strategy: str
    order_id: str
