from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional

class SymbolUniverse(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # The canonical symbol (normalized)
    symbol: str = Field(index=True, unique=True)

    # Where this symbol came from (IPO strategy, SP500, manual, etc.)
    source: str | None = None

    # Whether the symbol is currently active in the universe
    is_active: bool = Field(default=True)

    # When it was added
    added_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # When it was deactivated (if ever)
    deactivated_at: datetime | None = None
