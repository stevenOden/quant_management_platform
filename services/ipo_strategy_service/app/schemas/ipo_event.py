from sqlmodel import SQLModel
from datetime import datetime

class IPOEventResponse(SQLModel):
    id: int
    symbol: str
    # Raw IPO Data from Scraper or API
    ipo_date: datetime
    company_name: str

    # Strategy State Machine
    state: str
    discovered_at: datetime
    watching_since: datetime | None
    ready_since: datetime | None
    holding_since: datetime | None
    exited_at: datetime | None

    # Strategy metadata
    last_signal: str | None
    last_signal_at: datetime | None

    # Strategy parameters
    target_price: float | None
    stop_loss_price: float | None
    entry_price: float | None
    exit_price: float | None

    # Position Size
    position_num_share: float | None
    position_pnl: float | None