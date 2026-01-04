from datetime import date

import httpx

from app.models.ipo_event import IPOEvent
from app.enums.ipo_state import IPOState
from app.clients.data_service_client import DataServiceClient
from app.config import DATA_SERVICE_URL
from app.clients.execution_service_client import ExecutionServiceClient
from app.config import EXECUTION_SERVICE_URL


''' Pure strategy logic: takes price + IPOEvent, returns signals'''

data_service_client = DataServiceClient(DATA_SERVICE_URL)
execution_service_client = ExecutionServiceClient(EXECUTION_SERVICE_URL)

async def transition_to_buy_signal(event: IPOEvent, today: date) -> bool:
    '''Transition from State READY -> BUY_SIGNAL if today's closing price is all-time high'''
    if event.state == IPOState.READY:
        ## TODO make sure this doesn't get executed before market close
        ohlcv_data = await data_service_client.get_daily_ohlcv_data(event.symbol,today)
        if ohlcv_data.close > event.highest_close:
            return True
    return False

async def transition_to_holding(event: IPOEvent, today: date) -> bool:
    '''Transition from State BUY_SIGNAL -> HOLDING if buy order is executed properly'''
    if event.state == IPOState.BUY_SIGNAL:
        return True