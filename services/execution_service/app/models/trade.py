from sqlmodel import SQLModel, Field
from datetime import datetime, timezone

class Trade(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True) # let the db assign id
    symbol: str
    quantity: float
    price: float
    side: str # "BUY" or "SELL"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class SystemState(SQLModel, table = True):
    '''Table to store execution service system state for recording whether
    the service is out of sync with the portfolio service due to a failed update attempt.
    If the service is our of sync, the portfolio_sync_required falg will be true.
    The execution service will be restricted from executing any further trades until
    a portfolio re-sync is performed and this flag is reset to False'''
    id: int = Field(default=1, primary_key=True)
    portfolio_sync_required: bool = Field(default=False)