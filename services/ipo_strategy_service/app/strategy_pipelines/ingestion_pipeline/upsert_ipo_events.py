from sqlmodel import Session,select
from app.db import engine
from app.enums.ipo_state import IPOState
from app.models.ipo_event import IPOEvent
import logging

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
                        logger.info(f"Updating {key} for symbol {event["symbol"]} from {existing_value} to {value}")
                        print(f"Updating {key} for symbol {event["symbol"]} from {existing_value} to {value}")
                    setattr(existing, key, value)
                if different:
                    existing_state = getattr(existing, 'state')
                    setattr(existing, 'state', IPOState.DISCOVERED) # if the data was changed, reset to discovered to start strategy over
                    logger.info(f"Updating state for symbol {event["symbol"]} from {existing_state} to DISCOVERED")
                    print(f"Updating state for symbol {event["symbol"]} from {existing_state} to DISCOVERED")
            else:
                new_event = IPOEvent(**event)
                session.add(new_event)
                logger.info(f"{new_event.symbol} | {new_event.company_name} Added to IPOEvent. IPO Date: {new_event.ipo_date.date()} | Market Cap: {new_event.market_cap}")

            session.commit()