from datetime import datetime, timezone, date, timedelta
import logging
from sqlmodel import Session, select
from app.models.ipo_event import IPOEvent
from app.enums.ipo_state import IPOState
from app.strategy_pipelines.entry_evaluation_pipeline.entry_evaluation_pipeline_logic import transition_to_ready, transition_to_buy_signal
from app.clients.data_service_client import DataServiceClient
from app.clients.execution_service_client import ExecutionServiceClient
from app.db import engine
from app.utility import get_today_eastern_timezone

logger = logging.getLogger(__name__)

data_service_client = DataServiceClient()
execution_service_client = ExecutionServiceClient()

async def run_entry_evaluation_pipeline():
    '''Evaluate non-signal generating time based state transitions and data collection'''

    with Session(engine) as session:
        today = get_today_eastern_timezone()
        logger.info(f"Entry Evaluation pipeline started for {today}")


        # IPO_DAY -> READY Evaluation:
        # 0. Get the events in state IPO_DAY
        ipoday_events = session.exec(select(IPOEvent).where(IPOEvent.state==IPOState.IPO_DAY)).all()

        for event in ipoday_events:
            try:
                # 1. If today is ipo date and after market close (This is scheduled to run after market close)..
                if transition_to_ready(event,today):

                    # 2. Get the open and close of the ipo day
                    ohlcv_data = await data_service_client.get_daily_ohlcv_data(event.symbol,event.ipo_date.date())

                    ## DEBUG
                    # from datetime import timedelta
                    # ohlcv_data = await data_service_client.get_daily_ohlcv_data(event.symbol, today - timedelta(days = 3))
                    ## DEBUG

                    if ohlcv_data is not None:
                        event.ipo_price = ohlcv_data.open

                        # 3. Set the highest close to the max of the open or the close
                        event.highest_close = max(ohlcv_data.open,ohlcv_data.close)
                        event.highest_close_at = today

                        # 4. Transition to Ready
                        logger.info(f"{event.symbol}: IPO_DAY -> READY")
                        event.state = IPOState.READY
                        event.ready_since = today
                        session.add(event)
            except Exception as e:
                logger.exception(f"Error processing IPO_DAY -> READY for {event.symbol} | {e}")

        # 5. Commit changes made in IPO_DAY -> evaluation
        session.commit()


        # READY -> BUY_SIGNAL Evaluation:
        # 0. Get the events in state READY
        ready_events = session.exec(select(IPOEvent).where(IPOEvent.state==IPOState.READY)).all()

        for event in ready_events:
            try:
                ## DEBUG
                # from datetime import timedelta
                # today = today + timedelta(days=1)
                ## END_DEBUG

                # 0. We can only hold up to 20 poistions at one time, prioritized by market cap
                # TODO: How do should we handle market cap prioritization? Do we initiate a sell on a loser to add this new one?
                holding_events = session.exec(select(IPOEvent).where(IPOEvent.state == IPOState.HOLDING)).all()
                if len(holding_events) == 20:
                    logger.info(f"Holding 20 Positions. Cannot move {event.symbol} to BUY_SIGNAL")
                    # If we already have 20, keep the event in ready, if it hit its theoretical stop loss or take profit, move to missed
                    current_price = await data_service_client.get_current_price(event.symbol)
                    target_gain_pct = 20.0
                    target_price = (target_gain_pct + 100) / 100 * event.highest_close
                    stop_loss_pct = 10.0
                    stop_loss_price = (100 - stop_loss_pct) / 100 * event.highest_close

                    if current_price >= target_price:
                        logger.info(f"{event.symbol} hit profit target price. Moving to MISSED")
                        event.state = IPOState.MISSED
                        session.add(event)
                        continue
                    elif current_price <= stop_loss_price:
                        logger.info(f"{event.symbol} hit stop loss price. Moving to MISSED")
                        event.state = IPOState.MISSED
                        session.add(event)
                        continue

                # 1. If the symbol is ready and today is not it's ipo day and buy criteria are met
                if await transition_to_buy_signal(event,today):
                    logger.info(f"{event.symbol}: READY -> BUY_SIGNAL")
                    # 2. Transition the state to "BUY_SIGNAL"
                    event.state = IPOState.BUY_SIGNAL
                    # 3. Save the signal price
                    event.entry_signal_price = await data_service_client.get_current_price(event.symbol)
                    event.last_signal = "BUY"
                    event.last_signal_at = today
                    session.add(event)
            except Exception as e:
                logger.exception(f"Error processing READY -> BUY_SIGNAL for {event.symbol} | {e}")

        # 4. Commit changes in READY -> BUY_SIGNAL Evaluation
        session.commit()