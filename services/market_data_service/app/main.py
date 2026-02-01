import asyncio
import logging
from fastapi import FastAPI

from app.clients.data_service_client import DataServiceClient
from app.services.fetcher import fetch_latest_1m_bar
from app.services.watchlist_manager import WatchlistManager
from app.config import poll_interval_seconds
from app.routes.stream import router as streaming_router

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# 0. Initialize Classes
from app.services.publisher import publisher # Singleton created in file to avoid circular import with routes/stream
data_service_client = DataServiceClient()
watchlist_manager = WatchlistManager()

async def lifespan(app: FastAPI):

    # Start Background Task
    task = asyncio.create_task(market_data_loop())
    app.state.loop_task = task

    try:
        yield
    finally:
        # Cleanup on Shutdown
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

app = FastAPI(title="Market Data Service", lifespan=lifespan)
app.include_router(streaming_router)

async def market_data_loop():
    while True:
        try:
            # 1. Refesh watchlist from Data Service
            symbols = await data_service_client.get_intraday_watchlist()
            watchlist_manager.update(symbols)

            print(watchlist_manager.symbols)

            # 2. Fetch and publish latest data bar for each symbol
            for symbol in watchlist_manager.symbols:
                bar = await fetch_latest_1m_bar(symbol)
                if bar:
                    await publisher.publish(bar)

        except Exception as e:
            logger.exception(f"Error in market data loop {e}")

        await asyncio.sleep(poll_interval_seconds)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8004,
        reload=True,
        log_level="debug",
    )