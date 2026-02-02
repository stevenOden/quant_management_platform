from datetime import date
from app.models.ipo_event import IPOEvent
from app.enums.ipo_state import IPOState

def transition_to_ipo_day(event: IPOEvent, today: date) -> bool:
    '''Transition from State Watching -> IPO_DAY if today is the ipo date'''
    return (
            event.state == IPOState.WATCHING
            and event.ipo_date is not None
            and event.ipo_date.date() == today
    )

def transition_to_missed(event: IPOEvent, today: date) -> bool:
    '''Transition from State Watching -> IPO_DAY if today is the ipo date'''
    return (
            event.state == IPOState.WATCHING
            and event.ipo_date is not None
            and today > event.ipo_date.date()
    )