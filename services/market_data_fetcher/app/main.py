from .scheduler import run_scheduler, run_daily_scheduler

def load_symbols():
    # Hardcoded for testing

    # Later load from env, config file, or pull all from data service

    return ["AAPL", "MSFT", "GOOG", "TLT"]

if __name__ == "__main__":
    symbols = load_symbols()

    USE_DAILY = False

    if USE_DAILY:
        run_daily_scheduler(symbols)
    else:
        run_scheduler(symbols)