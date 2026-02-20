from pydantic import BaseModel

class Position(BaseModel):
    symbol: str
    quantity: float
    avg_cost: float
    last_price: float
    market_value: float
    unrealized_pnl: float
    strategy: str
    state: str
