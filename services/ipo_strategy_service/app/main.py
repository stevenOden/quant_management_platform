from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
import logging
from app.db import create_db_and_tables

from ingestion.ingestion_main import run_ipo_ingestion

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler_task = asyncio.create_task(scheduler_loop())
    logger.info("Scheduler started")
    create_db_and_tables()
    yield

    # Shutdown

    scheduler_task.cancel()
    logger.info("Scheduler stopped")

async def scheduler_loop():
    while True:
        try:
            await run_ipo_ingestion()
        except Exception as e:
            logger.exception(f"Error running IPO ingestion: {e}")

            # sleep 24 hours

            await asyncio.sleep(86400)

app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import asyncio
    create_db_and_tables()
    asyncio.run(run_ipo_ingestion())
