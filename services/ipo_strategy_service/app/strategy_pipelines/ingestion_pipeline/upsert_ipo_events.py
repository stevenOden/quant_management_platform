from sqlmodel import Session,select
from app.db import engine
from app.enums.ipo_state import IPOState
from app.models.ipo_event import IPOEvent
import logging

from app.utility import get_today_eastern_timezone

logger = logging.getLogger(__name__)

def upsert_ipo_events(events):
    with Session(engine) as session:
        for event in events:
            statement = (
                select(IPOEvent)
                .where(
                    IPOEvent.company_name == event["company_name"]
                )
            )

            result = session.exec(statement)
            existing = result.one_or_none()

            different = False
            if existing:
                for key, value in event.items():
                    # TODO: add check for difference in value at key and add to logging
                    existing_value = getattr(existing, key)
                    if value != existing_value:
                        different = True
                        logger.info(f'Updating {key} for symbol {event["symbol"]} from {existing_value} to {value}')
                        print(f'Updating {key} for symbol {event["symbol"]} from {existing_value} to {value}')
                    setattr(existing, key, value)
                if different:
                    # Ignore changes if today is still the ipo_day (market cap is updated constantly as the stock ipos)
                    if existing.ipo_date.date() != get_today_eastern_timezone():
                        existing_state = getattr(existing, 'state')
                        setattr(existing, 'state', IPOState.DISCOVERED) # if the data was changed, reset to discovered to start strategy over
                        logger.info(f'Updating state for symbol {event["symbol"]} from {existing_state} to DISCOVERED')
                        print(f'Updating state for symbol {event["symbol"]} from {existing_state} to DISCOVERED')
                        session.add(existing)
                    else:
                        logger.info(f"Today is ipo day, ignoring changes")
                        print(f"Today is ipo day, ignoring changes")
            else:
                new_event = IPOEvent(**event)
                session.add(new_event)
                logger.info(f"{new_event.symbol} | {new_event.company_name} Added to IPOEvent. IPO Date: {new_event.ipo_date.date()} | Market Cap: {new_event.market_cap}")

            session.commit()