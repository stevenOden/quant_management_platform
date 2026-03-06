from sqlmodel import SQLModel, Field
from datetime import datetime,date

class DailyPnl(SQLModel, table=True):
    datestamp: date = Field(primary_key=True)
    realized_pnl: float
    unrealized_pnl: float
    total_pnl: float
    portfolio_value: float
