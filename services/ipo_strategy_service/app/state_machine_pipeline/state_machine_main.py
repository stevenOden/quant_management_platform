from datetime import datetime, timezone, date, timedelta
import logging
from sqlmodel import Session, select
from app.models.ipo_event import IPOEvent
from app.enums.ipo_state import IPOState
from app.state_machine_pipeline.state_machine_logic import transition_to_ipo_day, transition_to_ready, transition_to_missed
from app.clients.data_service_client import DataServiceClient
from app.config import DATA_SERVICE_URL
from app.db import engine

logger = logging.getLogger(__name__)

data_service_client = DataServiceClient(DATA_SERVICE_URL)

def get_today_utc() -> date:
    return datetime.now(timezone.utc).date()

def get_tomorrow():
    return (datetime.now(timezone.utc) + timedelta(days=1)).date()

def get_yesterday(event):
    return (event.ipo_date - timedelta(days=1)).date()

async def run_state_machine_pipeline():
    '''Evaluate non-signal generating time based state transitions and data collection'''

    with Session(engine) as session:
        today = get_today_utc()
        logger.info(f"State machine pipeline started for {today}")

        watch_events = session.exec(select(IPOEvent).where(IPOEvent.state==IPOState.WATCHING)).all()

        for event in watch_events:
            try:
                if transition_to_ipo_day(event,today):
                    logger.info(f"{event.symbol}: WATCHING -> IPO_DAY")
                    event.state = IPOState.IPO_DAY
                    session.add(event)
                elif transition_to_missed(event,today):
                    logger.info(f"{event.symbol}: WATCHING -> MISSED")
                    event.state = IPOState.MISSED
                    session.add(event)
            except Exception:
                logger.exception(f"Error processing state machine for {event.symbol}")
        ## DEBUG
        today= get_tomorrow()
        ## END_DEBUG

        ipoday_events = session.exec(select(IPOEvent).where(IPOEvent.state==IPOState.IPO_DAY)).all()

        for event in ipoday_events:
            try:
                if transition_to_ready(event,today):
                    ## DEBUG
                    ohlcv_data = await data_service_client.get_daily_ohlcv_data(event.symbol, get_today_utc())
                    ## END_DEBUG
                    # ohlcv_data = await data_service_client.get_daily_ohlcv_data(event.symbol,event.ipo_date.date())
                    if ohlcv_data is not None:
                        event.ipo_price = ohlcv_data.open
                        event.highest_close = max(ohlcv_data.open,ohlcv_data.close)
                        event.highest_close_at = datetime.now(timezone.utc)
                        logger.info(f"{event.symbol}: IPO_DAY -> READY")
                        event.state = IPOState.READY
                        event.ready_since = datetime.now(timezone.utc)
                        session.add(event)
                    # record open and close for the day
            except Exception:
                logger.exception(f"Error processing state machine for {event.symbol}")

        session.commit()
