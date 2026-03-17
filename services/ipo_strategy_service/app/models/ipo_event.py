from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from app.utility import get_time_eastern_timezone

class IPOEvent(SQLModel, table=True):

    id: int | None = Field(default=None, primary_key=True)

    # Raw IPO Data from Scraper or API
    ipo_date: datetime
    symbol: str | None = Field(default=None, index=True)
    company_name: str
    exchange: str | None
    price_low: float | None
    price_high: float | None
    shares_offered: int | None
    deal_size: float | None
    market_cap: float | None
    revenue: float | None

    # Strategy State Machine
    state: str = Field(default="DISCOVERED") # DISCOVERED, WATCHING, READY, BUY_SIGNAL, HOLDING, EXITED
    discovered_at: datetime = Field(default_factory=lambda: get_time_eastern_timezone())
    watching_since: datetime | None = None # Default to None on DISCOVERY State
    ready_since: datetime | None = None # Default to None on DISCOVERY State
    holding_since: datetime | None = None # Default to None on DISCOVERY State
    exited_at: datetime | None = None # Default to None on DISCOVERY State

    # Strategy metadata
    last_signal: str | None = None # Default to None on DISCOVERY State
    last_signal_at: datetime | None = None # Default to None on DISCOVERY State
    last_trade_id: str | None = None # Default to None on DISCOVERY State
    entry_trade_id: int | None = None # Default to None on DISCOVERY State
    exit_trade_id: int | None = None # Default to None on DISCOVERY State
    last_trade_at: datetime | None = None # Default to None on DISCOVERY State
    ipo_price: float | None = None # Default to None on DISCOVERY State
    highest_close: float | None = None # Default to None on DISCOVERY State
    highest_close_at: datetime | None = None # Default to None on DISCOVERY State

    # Strategy parameters (optional but useful)
    target_gain_pct: float | None = None # Default to None on DISCOVERY State
    target_price: float | None = None # Default to None on DISCOVERY State
    stop_loss_pct: float | None = None # Default to None on DISCOVERY State
    stop_loss_price: float | None = None # Default to None on DISCOVERY State
    entry_price: float | None = None # Default to None on DISCOVERY State
    entry_signal_price: float | None = None # Default to None on DISCOVERY State
    exit_price: float | None = None # Default to None on DISCOVERY State
    exit_signal_price: float | None = None # Default to None on DISCOVERY State

    # Position Size
    position_num_share: float | None = None # Default to None on DISCOVERY State
    position_entry_value: float | None = None # Default to None on DISCOVERY State
    position_exit_value: float | None = None # Default to None on DISCOVERY State
    position_pnl: float | None = None # Default to None on DISCOVERY State

    current_price : float | None = None # Default to None on DISCOVERY State

