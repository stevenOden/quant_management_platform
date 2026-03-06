import time
import logging.config
import yaml
from pathlib import Path
from app.fetchers.fetcher import trigger_data_service_fetch, trigger_data_service_ohlcv_fetch
from app.clients.data_service_client import get_symbols_from_universe, get_health_status
from app.config import FETCH_INTERVAL_SECONDS
from requests.exceptions import HTTPError
from app.utility import get_today_eastern_timezone, get_time_eastern_timezone, market_close, tomorrow_close

config_path = Path(__file__).parent / "logging.yaml"
with config_path.open("r") as fin:
    config = yaml.safe_load(fin)
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

def run_daily_scheduler():
    """Production EOD schedular."""
    last_ingest_date = None

    while True:
        today = get_today_eastern_timezone()
        ## DEBUG
        from datetime import timedelta
        today = today - timedelta(days=5)
        ## END_DABUG
        now = get_time_eastern_timezone()

        # Add retry loop to wait for data service to be up
        if not last_ingest_date:
            get_health_status()

        # If it's past EOD and we haven't ingested today
        if now >= market_close and last_ingest_date != now.date():
            print(f"--- Running end-of-day OHLCV ingestion at {now.strftime('%Y-%m-%d %H:%M')} ---")
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
                    except HTTPError as e:
                        if e.response is not None and e.response.status_code == 404:
                            logger.info(f"Data not found for {symbol}")
                        else:
                            logger.exception(f"Error for symbol {symbol}: {e}")
                    except Exception as e:
                        logger.exception(f"Error for symbol {symbol}: {e}")
            except Exception as e:
                logger.exception(f"Error in market data fetching loop: {e}")

            last_ingest_date = now.date()
        if market_close > now:
            sleep_time = (market_close - now).seconds
        else:
            sleep_time = (tomorrow_close - now).seconds
        hours,minutes = divmod(sleep_time,3600)
        minutes = int(round(minutes/60,0))
        logger.info(f"Sleeping for {sleep_time} seconds | {hours} hours {minutes} minutes")
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
