from datetime import timedelta
from math import floor
from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
import asyncio

from app.db import create_db_and_tables
from app.routes.ipo_events import router as ipo_event_router
from app.strategy_pipelines.buy_signal_pipeline.buy_signal_pipeline_main import run_buy_signal_pipeline

from app.strategy_pipelines.ingestion_pipeline.ingestion_pipeline_main import run_ipo_ingestion_pipeline
from app.strategy_pipelines.ipo_day_pipeline.ipo_day_pipeline_main import run_ipo_day_pipeline
from app.strategy_pipelines.universe_pipeline.universe_pipeline_main import run_universe_pipeline
from app.strategy_pipelines.entry_evaluation_pipeline.entry_evaluation_pipeline_main import run_entry_evaluation_pipeline
from app.strategy_pipelines.exit_evaluation_pipeline.exit_evaluation_main import run_exit_evaluation_pipeline
from app.utility import market_close, market_close_delayed, market_close_plus1, market_open, market_open_plus1, get_time_eastern_timezone, tomorrow_open

root = logging.getLogger()
for handler in root.handlers:
    handler.setLevel(logging.INFO)

logger = logging.getLogger(__name__)




@asynccontextmanager
async def lifespan(app: FastAPI):
    entry_task = asyncio.create_task(entry_loop())
    exit_task = asyncio.create_task(exit_loop())
    create_db_and_tables()
    yield

    # Shutdown
    entry_task.cancel()
    exit_task.cancel()
    logger.info("Scheduler stopped")

async def entry_loop():
    '''
    Evaluate Ingestion, Universe, IPO Day every hour
    Evaluate Entry Evaluation once after market close
    Evaluate Buy Signal once after market Open
    '''
    logger.info("Entry Loop started")
    while True:
        try:
            # 0. Get the current time in eastern time zone (DST tolerant)
            now = get_time_eastern_timezone()

            # 1. In the hour of market open, run the buy signal pipeline
            if now >= market_open and now < market_open_plus1:
                await run_buy_signal_pipeline()
                logger.info("Buy Signal pipeline completed")

            # 2. In the hour after market close, run the entry evaluation pipeline
            elif now >= market_close_delayed and now < market_close_plus1:
                await run_entry_evaluation_pipeline()
                logger.info("Entry Evaluation pipeline completed")

            # 3. Every hour run the ingestion, universe and ipo day pipelines
            await run_ipo_ingestion_pipeline()
            logger.info("IPO ingestion pipeline completed")
            await run_universe_pipeline()
            logger.info("Universe pipeline completed")
            await run_ipo_day_pipeline()
            logger.info("IPO Day pipeline completed")

        except Exception as e:
            logger.exception(f"Error in Entry Loop: {e}")

        # sleep 1 hour
        logger.info("Entry Loop Sleeping for 30 minutes")
        await asyncio.sleep(1800)

async def exit_loop():
    '''Evaluate Exit Evaluation Pipeline continuously during market hours'''
    logger.info("Exit Loop started")
    while True:
        try:
            now = get_time_eastern_timezone()

            # Limit this to during market hours for now
            if now >= market_open and now <= market_close:
                await run_exit_evaluation_pipeline()
            else:
                sleeptime = floor((market_open - now).seconds /3600)
                if sleeptime < 0: # If we are after market wait for tomorrow's open, if we are in the morning wait for today's
                    sleeptime = floor((tomorrow_open - now).seconds /3600)
                logger.info(f"Exit Loop Sleeping for {sleeptime} hours")
                await asyncio.sleep(sleeptime * 3600)

        except Exception as e:
            logger.exception(f"Error in Exit Loop: {e}")

app = FastAPI(lifespan=lifespan)
app.include_router(ipo_event_router)

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import asyncio
    create_db_and_tables()
    asyncio.run(run_ipo_ingestion_pipeline()) # get new ipos from web
    # asyncio.run(run_universe_pipeline()) # adds new ipos to symbol universe
    # asyncio.run(run_ipo_day_pipeline()) # evaluates if the symbols hit ipo date and then records the highest close
    # asyncio.run(run_entry_evaluation_pipeline()) # evaluates the close price and then submits trade order
    # asyncio.run(run_buy_signal_pipeline())
    # asyncio.run(run_exit_evaluation_pipeline())