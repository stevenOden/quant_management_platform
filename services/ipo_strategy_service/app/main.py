from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
import logging
from app.db import create_db_and_tables
from app.routes.ipo_events import router as ipo_event_router

from app.ingestion_pipeline.ingestion_pipeline_main import run_ipo_ingestion_pipeline
from app.universe_pipeline.universe_pipeline_main import run_universe_pipeline
from app.state_machine_pipeline.state_machine_main import run_state_machine_pipeline

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
            # 1. Run IPO Ingestion Pipeline
            await run_ipo_ingestion_pipeline()
            logger.info("IPO ingestion pipeline completed")

            # 2. Run Universe pipeline (register new IPO symbols to SymbolUniverse Table)
            await run_universe_pipeline()
            logger.info("Universe pipeline completed")

        except Exception as e:
            logger.exception(f"Error scheduler loop: {e}")

        # sleep 24 hours
        await asyncio.sleep(86400)

app = FastAPI(lifespan=lifespan)
app.include_router(ipo_event_router)

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import asyncio
    create_db_and_tables()
    # asyncio.run(run_ipo_ingestion_pipeline())
    # asyncio.run(run_universe_pipeline())
    asyncio.run(run_state_machine_pipeline())
