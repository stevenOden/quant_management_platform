from datetime import date
from app.models.ipo_event import IPOEvent
from app.enums.ipo_state import IPOState
from app.clients.data_service_client import DataServiceClient
from app.clients.execution_service_client import ExecutionServiceClient
from app.utility import get_time_eastern_timezone, market_close

data_service_client = DataServiceClient()
execution_service_client = ExecutionServiceClient()

def transition_to_ready(event: IPOEvent, today: date) -> bool:
    '''Transition from state IPO_DAY -> READY once ipo day has passed'''
    return (
        event.state == IPOState.IPO_DAY
        and event.ipo_date is not None
        and today == event.ipo_date.date()
        and get_time_eastern_timezone() >= market_close
    )

async def transition_to_buy_signal(event: IPOEvent, today: date) -> bool:
    '''Transition from State READY -> BUY_SIGNAL if today's closing price is all-time high'''
    if event.state == IPOState.READY and today > event.ipo_date.date() and get_time_eastern_timezone() >= market_close:
        ohlcv_data = await data_service_client.get_daily_ohlcv_data(event.symbol,today)

        ## DEBUG
        ohlcv_data.close += 10

        ## END_DEBUG
        if ohlcv_data.close > event.highest_close:
            return True
    return False