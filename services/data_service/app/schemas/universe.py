from sqlmodel import SQLModel

class SymbolRequest(SQLModel):
    symbol: str
    source: str | None = None