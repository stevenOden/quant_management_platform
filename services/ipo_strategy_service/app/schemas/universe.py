from sqlmodel import SQLModel
from datetime import datetime

class SymbolResponse(SQLModel):
    id: int
    symbol: str
    source: str
    is_active: bool
    added_at: datetime
    deactivated_at: datetime | None

class IntradaySymbolResponse(SQLModel):
    id: int
    symbol: str
    source: str
    added_at: datetime