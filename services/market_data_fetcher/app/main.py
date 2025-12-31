from app.scheduler import run_scheduler, run_daily_scheduler

if __name__ == "__main__":

    USE_DAILY = False

    if USE_DAILY:
        run_daily_scheduler()
    else:
        run_scheduler()