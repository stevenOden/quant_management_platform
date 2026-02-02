from datetime import datetime, timezone, date, timedelta
import logging
from sqlmodel import Session, select
from app.models.ipo_event import IPOEvent
from app.enums.ipo_state import IPOState
from app.strategy_pipelines.buy_signal_pipeline.buy_signal_pipeline_logic import transition_to_holding
from app.clients.data_service_client import DataServiceClient
from app.clients.execution_service_client import ExecutionServiceClient
from app.db import engine
from app.utility import get_today_eastern_timezone

logger = logging.getLogger(__name__)

data_service_client = DataServiceClient()
execution_service_client = ExecutionServiceClient()

async def run_buy_signal_pipeline():
    today = get_today_eastern_timezone()
    logger.info(f"Buy Signal pipeline started for {today}")
    with Session(engine) as session:

        # BUY_SIGNAL -> HOLDING Evaluation:
        # 0. Get events in state BUY_SIGNAL
        buy_signal_events = session.exec(select(IPOEvent).where(IPOEvent.state == IPOState.BUY_SIGNAL)).all()

        for event in buy_signal_events:
            try:
                # 1. Transition to holding if the state is BUY_SIGNAL and today is not the IPO_DAY (Redundant)
                if await transition_to_holding(event, today):

                    # 2. Calculate the quantity to buy (Currently fixed position size)
                    set_position_value = 1000.00  # TODO make this fraction of portfolio value
                    current_price = await data_service_client.get_current_price(event.symbol)
                    if not current_price:
                        return False
                    quantity = set_position_value / current_price

                    # 3. Calculate Stop Loss and Take Profit values
                    event.target_gain_pct = 20.0
                    event.target_price = (event.target_gain_pct + 100) / 100 * current_price
                    event.stop_loss_pct = 10.0
                    event.stop_loss_price = (100 - event.stop_loss_pct) / 100 * current_price

                    # 4. Execute Buy Order (Later include stoploss and Take Profit in IBKR order)
                    trade_info = await execution_service_client.execute_trade(event.symbol, quantity, "BUY")  # 10s timeout
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
                    session.commit()

            except Exception as e:
                logger.exception(f"Error processing Buy Signal Pipeline for {event.symbol} | {e}")