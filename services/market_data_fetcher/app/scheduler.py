import time
import datetime
from .fetcher import trigger_data_service_fetch
from .config import FETCH_INTERVAL_SECONDS

END_OF_DAY_HOUR = 16 # 4pm ET
CHECK_INTERVAL_SECONDS = 3600 # check if it's time to ingest once per hour

def run_scheduler(symbols: list[str]):
    """Fast loop schedular for testing purposes."""
    while True:
        for symbol in symbols:
            try:
                result = trigger_data_service_fetch(symbol)
                print(f"Ingested {symbol}: {result}")
            except Exception as e:
                print(f"Error fetching {symbol}: {e}")

        time.sleep(FETCH_INTERVAL_SECONDS)

def run_daily_scheduler(symbols: list[str]):
    """Production EOD schedular."""
    last_ingest_date = None

    while True:
        now = datetime.datetime.now()

        # If it's past EOD and we haven't ingested today
        if now.hour >= END_OF_DAY_HOUR and last_ingest_date != now.date():
            print("Running end-of-day ingestion...")
            for symbol in symbols:
                try:
                    result = trigger_data_service_fetch(symbol)
                    print(f"Ingested {symbol}: {result}")
                except Exception as e:
                    print(f"Error ingesting {symbol}: {e}")

            last_ingest_date = now.date()

        time.sleep(CHECK_INTERVAL_SECONDS)
