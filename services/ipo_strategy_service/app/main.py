from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
from app.db import create_db_and_tables
from app.routes.ipo_events import router as ipo_event_router

from app.strategy_pipelines.ingestion_pipeline.ingestion_pipeline_main import run_ipo_ingestion_pipeline
from app.strategy_pipelines.universe_pipeline.universe_pipeline_main import run_universe_pipeline
from app.strategy_pipelines.state_machine_pipeline.state_machine_main import run_state_machine_pipeline
from app.strategy_pipelines.evaluation_pipeline.evaluation_pipeline_main import run_evaluation_pipeline
from app.strategy_pipelines.exit_evaluation_pipeline.exit_evaluation_main import run_exit_evaluation_pipeline
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # exit_task = asyncio.create_task(run_exit_evaluation_pipeline())
    # scheduler_task = asyncio.create_task(scheduler_loop())
    logger.info("Scheduler started")
    create_db_and_tables()
    yield

    # Shutdown
    # scheduler_task.cancel()
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
    # asyncio.run(run_ipo_ingestion_pipeline()) # get new ipos from web
    # asyncio.run(run_universe_pipeline()) # adds new ipos to symbol universe
    # asyncio.run(run_state_machine_pipeline()) # evaluates if the symbols hit ipo date and then records the highest close
    # asyncio.run(run_evaluation_pipeline()) # evaluates the close price and then submits trade order
    asyncio.run(run_exit_evaluation_pipeline())

    # Every hour - ingestion pipeline, universe pipeline, ipo_day pipeline
    # new ipo ingestion should be run every hour in case an ipo date is updated mid day
    # universe is always run right after ipo ingestion
    # ipo day check should run after incase an ipo date was updated #TODO seperate out ipo_day pipeline


    # After market close - entry_evaluation pipeline ipo_day -> buy signal
    # ido_day -> ready check should always just run after market close - only depends on the closing price
    # ready -> buy_signal run after market close - looks for new highest close #TODO add check for sync flag? do not signal trades if cannot be executed? i think this is the right spot, becasue can re-evaluate next close > highest close; strategy intact?
    # TODO combine ipo_day->ready and ready -> buy_signal into entry_evaluation pipeline


    # Market open - entry_execution pipeline
    # buy -> holding - execute the buy at market open, #TODO add check for sync flag? do not send trades if cannot be executed; strategy not intact if currentclose < highest close?
    # TODO move buy -> holding to entry_execution pipeline


    # Constantly - exit_evaluation pipeline -> holding -> exit_signal
    # Holding -> Exit signal - generate the exit signal, in case something goes wrong with execution, signal is saved and not re-evaluated
    # Exit_signal -> closed ?? not sure about this one yet