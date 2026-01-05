from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional

class IntradayWatchlist(SQLModel, table=True):
    '''Symbols also in the Symbol Universe that require more granular intraday data for strategy evaluation.
    Intraday data is served by the market data service. Each strategy/service currently using intraday data for a particular
    symbol will have a row. When a strategy/service no longer needs ntraday data for the symbol it will remove its row.
    '''
    id: Optional[int] = Field(default=None, primary_key=True)

    # The canonical symbol (normalized)
    symbol: str = Field(index=True)

    # Where this symbol came from (IPO strategy, SP500, manual, etc.)
    source: str | None = None

    # When it was added
    added_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
