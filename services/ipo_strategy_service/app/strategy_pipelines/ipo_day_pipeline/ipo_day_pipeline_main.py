from datetime import datetime, timezone, date, timedelta
import logging
from sqlmodel import Session, select
from app.models.ipo_event import IPOEvent
from app.enums.ipo_state import IPOState
from app.db import engine
from app.utility import get_today_eastern_timezone

from app.strategy_pipelines.ipo_day_pipeline.ipo_day_pipeline_logic import transition_to_ipo_day, transition_to_missed

logger = logging.getLogger(__name__)

async def run_ipo_day_pipeline():
    with Session(engine) as session:
        today = get_today_eastern_timezone()
        logger.info(f"IPO Day pipeline started for {today}")

        watch_events = session.exec(select(IPOEvent).where(IPOEvent.state==IPOState.WATCHING)).all()

        for event in watch_events:
            try:
                if transition_to_ipo_day(event ,today): # If today is the day of the IPO
                    logger.info(f"{event.symbol}: WATCHING -> IPO_DAY")
                    event.state = IPOState.IPO_DAY
                    session.add(event)
                elif transition_to_missed(event ,today): # If the Ipo date is passed, and we didn't watch the price
                    logger.info(f"{event.symbol}: WATCHING -> MISSED")
                    event.state = IPOState.MISSED
                    session.add(event)
            except Exception:
                logger.exception(f"Error processing state machine for {event.symbol}")

            session.commit()