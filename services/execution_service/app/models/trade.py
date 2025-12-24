from sqlmodel import SQLModel, Field
from datetime import datetime, timezone

class Trade(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True) # let the db assign id
    symbol: str
    quantity: float
    price: float
    side: str # "BUY" or "SELL"

    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))