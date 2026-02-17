import time
import logging
from app.fetchers.fetcher import trigger_data_service_fetch, trigger_data_service_ohlcv_fetch
from app.clients.data_service_client import get_symbols_from_universe
from app.config import FETCH_INTERVAL_SECONDS
from datetime import datetime,date,timezone
from app.utility import get_today_eastern_timezone, get_time_eastern_timezone, market_close, tomorrow_close

logger = logging.getLogger(__name__)

def run_daily_scheduler():
    """Production EOD schedular."""
    last_ingest_date = None

    while True:
        today = get_today_eastern_timezone()
        now = get_time_eastern_timezone()

        # If it's past EOD and we haven't ingested today
        if now >= market_close and last_ingest_date != now.date():
            print("Running end-of-day ingestion...")
            try:
                symbols = get_symbols_from_universe()
                for symbol in symbols:
                    try:
                        logger.info(f"Fetching price for {symbol}")
                        result = trigger_data_service_fetch(symbol)
                        logger.info(f"Ingested Price for {symbol}: {result}")
                        logger.info(f"Fetching OHLCV data for {today}")
                        result = trigger_data_service_ohlcv_fetch(symbol,today)
                        logger.info(f"Ingested OHLCV data for {symbol}: {result}")
                    except Exception as e:
                        logger.exception(f"Error for symbol {symbol}: {e}")
            except Exception as e:
                logger.exception(f"Error in market data fetching loop: {e}")

            last_ingest_date = now.date()
        if market_close > now:
            sleep_time = (market_close - now).seconds
        else:
            sleep_time = (tomorrow_close - now).seconds
        time.sleep(sleep_time)

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
