from pydantic import BaseModel
from datetime import datetime, date

class StrategyState(BaseModel):
    symbol: str
    strategy: str
    state: str
    ipo_date: date
    entry_price: float | None
    entry_value: float | None
    target_price: float | None
    stop_loss: float | None
    pnl: float | None
    pnl_percent: float | None
    last_evaluated: datetime | None

class IPOStateResponse(BaseModel):
    DISCOVERED: list[StrategyState]
    WATCHING: list[StrategyState]
    IPO_DAY: list[StrategyState]
    READY: list[StrategyState]
    BUY_SIGNAL: list[StrategyState]
    SELL_SIGNAL: list[StrategyState]
    HOLDING: list[StrategyState]
    EXITED: list[StrategyState]
    MISSED: list[StrategyState]
