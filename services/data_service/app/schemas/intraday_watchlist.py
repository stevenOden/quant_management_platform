from sqlmodel import SQLModel

class IntradayWatchlistRequest(SQLModel):
    symbol: str
    source: str | None = None