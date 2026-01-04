import time
import logging
import datetime
from app.fetchers.fetcher import trigger_data_service_fetch, trigger_data_service_ohlcv_fetch
from app.clients.data_service_client import get_symbols_from_universe
from app.config import FETCH_INTERVAL_SECONDS
from datetime import datetime,date,timezone

logger = logging.getLogger(__name__)

END_OF_DAY_HOUR = 16 # 4pm ET
CHECK_INTERVAL_SECONDS = 3600 # check if it's time to ingest once per hour
default_symbols = ['AAPL','MSFT','GOOG'] # for testing

today = datetime.now(timezone.utc).date()

def run_daily_scheduler():
    """Production EOD schedular."""
    last_ingest_date = None

    while True:
        now = datetime.datetime.now() #TODO: UPDATE THIS FOR UTC TIME AND DAYLIGHT SAVINGS

        # If it's past EOD and we haven't ingested today
        if now.hour >= END_OF_DAY_HOUR and last_ingest_date != now.date():
            print("Running end-of-day ingestion...")
            try:
                symbols = get_symbols_from_universe()
                for entry in symbols:
                    symbol = entry['symbol']
                    logger.info(f"Fetching price for {symbol}")
                    result = trigger_data_service_fetch(symbol)
                    logger.info(f"Ingested Price for {symbol}: {result}")
                    logger.info(f"Fetching OHLCV data for {today}")
                    result = trigger_data_service_ohlcv_fetch(symbol,today)
                    logger.info(f"Ingested OHLCV data for {symbol}: {result}")
            except Exception as e:
                logger.exception(f"Error in market data fetching loop: {e}")

            last_ingest_date = now.date()

        time.sleep(CHECK_INTERVAL_SECONDS)

def run_scheduler():
    """Fast loop schedular for testing purposes."""
    while True:
        try:
            symbols = get_symbols_from_universe()
            for entry in symbols:
                symbol = entry['symbol']
                logger.info(f"Fetching price for {symbol}")
                result = trigger_data_service_fetch(symbol)
                logger.info(f"Ingested {symbol}: {result}")
                logger.info(f"Fetching OHLCV data for {today}")
                result = trigger_data_service_ohlcv_fetch(symbol, today)
                logger.info(f"Ingested OHLCV data for {symbol}: {result}")
        except Exception as e:
            logger.exception(f"Error in market data fetching loop: {e}")

        time.sleep(FETCH_INTERVAL_SECONDS)
