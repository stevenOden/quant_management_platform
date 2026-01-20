from datetime import datetime, timezone, date, timedelta
import logging
from sqlmodel import Session, select
from app.models.ipo_event import IPOEvent
from app.enums.ipo_state import IPOState
from app.strategy_pipelines.evaluation_pipeline.evaluation_pipeline_logic import transition_to_buy_signal, transition_to_holding
from app.clients.data_service_client import DataServiceClient
from app.clients.execution_service_client import ExecutionServiceClient

from app.db import engine

logger = logging.getLogger(__name__)

data_service_client = DataServiceClient()
execution_service_client = ExecutionServiceClient()

def get_today_utc() -> date:
    return datetime.now(timezone.utc).date()

def get_today_current_timezone() -> date:
    return datetime.now().date()

def get_tomorrow():
    return (datetime.now(timezone.utc) + timedelta(days=1)).date()

def get_yesterday():
    return (datetime.now() - timedelta(days=1)).date()

async def run_evaluation_pipeline():
    '''Evaluate non-signal generating time based state transitions and data collection'''

    with Session(engine) as session:
        # today = get_today_utc()
        # today = get_today_current_timezone()
        today = get_yesterday()
        logger.info(f"State machine pipeline started for {today}")

        ready_events = session.exec(select(IPOEvent).where(IPOEvent.state==IPOState.READY)).all()

        for event in ready_events:
            try:
                if await transition_to_buy_signal(event,today):
                    logger.info(f"{event.symbol}: READY -> BUY_SIGNAL")
                    event.state = IPOState.BUY_SIGNAL
                    event.entry_signal_price = await data_service_client.get_current_price(event.symbol)
                    ## DEBUG
                    # event.entry_signal_price+=10
                    ## END_DEBUG
                    event.last_signal = "BUY"
                    event.last_signal_at = today
                    session.add(event)
            except Exception:
                logger.exception(f"Error processing state machine for {event.symbol}")

        buy_signal_events = session.exec(select(IPOEvent).where(IPOEvent.state==IPOState.BUY_SIGNAL)).all()

        for event in buy_signal_events:
            try:
                if await transition_to_holding(event,today):
                    '''This will not commit unless the trade info is returned correctly from execution service'''

                    # 1. Calculate the quantity based off fixed position size and current price
                    set_position_value = 1000.00  # TODO make this fraction of portfolio value
                    current_price = await data_service_client.get_current_price(event.symbol)
                    if not current_price:
                        return False
                    quantity = set_position_value / current_price

                    #2. Calculate Stop Loss and Take Profit values
                    event.target_gain_pct = 20.0
                    event.target_price = (event.target_gain_pct+100)/100 * current_price
                    event.stop_loss_pct = 10.0
                    event.stop_loss_price = (100 - event.stop_loss_pct)/100 * current_price

                    # 3. Execute Buy Order (Later include stoploss and Take Profit)
                    trade_info = await execution_service_client.execute_trade(event.symbol, quantity, "BUY") # 10s timeout
                    # TODO: IBKR allows bracket orders that send the stop loss and take profit orders with the buy order
                    #  In order to simulate that without using IBKR we can stream the prices for symbols in the portfolio

                    # 4. Log Trade Execution Details (will fail if trade not executed properly)
                    event.entry_price = trade_info.price
                    event.position_num_share = trade_info.quantity
                    event.position_entry_value = trade_info.price * trade_info.quantity
                    # TODO Save off trade_id -> add to sql model
                    event.state = IPOState.HOLDING
                    event.holding_since = datetime.now()
                    # TODO: What to do if the portfolio and execution service become unsynced? No more trades will be placed, but cannot sell current positions

                    # 5. Update the IntradayWatchlist to add this symbol to the intraday stream
                    intraday_watch = await data_service_client.add_intraday_watchlist_symbol(event.symbol)
                    if intraday_watch:
                        session.add(event)

            except Exception:
                logger.exception(f"Error processing state machine for {event.symbol}")

        session.commit()