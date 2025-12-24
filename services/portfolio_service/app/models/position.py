from sqlmodel import SQLModel, Field

class Position(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    symbol: str
    quantity: float
    average_cost: float