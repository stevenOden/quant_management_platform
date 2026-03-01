from pydantic import BaseModel
from datetime import datetime
class StrategyState(BaseModel):
    symbol: str
    strategy: str
    state: str
    entry_price: float | None
    target_price: float | None
    stop_loss: float | None
    last_evaluated: datetime
