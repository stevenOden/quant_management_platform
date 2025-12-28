from sqlmodel import SQLModel, Field

class Position(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    symbol: str
    quantity: float
    average_cost: float
    last_trade_id: int | None = Field(default=None) # can be int or None, starts as None before any trades processed