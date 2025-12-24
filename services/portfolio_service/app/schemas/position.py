from sqlmodel import SQLModel

class PositionCreate(SQLModel):
    symbol: str
    quantity: float
    average_cost: float

class PositionRead(SQLModel):
    symbol: str
    quantity: float
    average_cost: float