from sqlmodel import Session,select
from ..db import engine
from ..models.ipo import IPOEvent

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

            if existing:
                for key, value in event.items():
                    setattr(existing, key, value)
            else:
                new_event = IPOEvent(**event)
                session.add(new_event)

            session.commit()