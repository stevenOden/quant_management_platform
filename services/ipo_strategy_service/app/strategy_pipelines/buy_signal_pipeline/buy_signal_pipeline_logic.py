from datetime import date
from app.models.ipo_event import IPOEvent
from app.enums.ipo_state import IPOState


async def transition_to_holding(event: IPOEvent, today: date) -> bool:
    '''Transition from State BUY_SIGNAL -> HOLDING if buy order is executed properly'''
    if event.state == IPOState.BUY_SIGNAL and today != event.ipo_date.date():
        return True