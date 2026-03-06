from sqlmodel import SQLModel, Field

class CashBalance(SQLModel, table=True):
    id: int = Field(default=1, primary_key=True)
    amount: float