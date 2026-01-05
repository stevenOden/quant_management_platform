import asyncio
import logging
from fastapi import FastAPI

from app.config import settings
from app.clients.data_service_client import DataServiceClient
from app.services.fetcher import fetch_latest_1m_bar
from app.services.publisher import LoggingMarketDataPublisher, MarketDataPublisher
from app.services.watchlist_manager import WatchlistManager

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def lifespan(app: FastAPI):
    # Initialize shared components
    data_service_client = DataServiceClient(settings.data_service_base_url)
    publisher: MarketDataPublisher = LoggingMarketDataPublisher()
    watchlist_manager = WatchlistManager()

    app.state.data_service_client = data_service_client
    app.state.publisher = publisher
    app.state.watchlist_manager = watchlist_manager

    # Start Background Task
    task = asyncio.create_task(
        market_data_loop(
            data_service_client = data_service_client,
            publisher = publisher,
            watchlist_manager = watchlist_manager
        )
    )
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

async def market_data_loop(
        data_service_client: DataServiceClient,
        publisher: MarketDataPublisher,
        watchlist_manager: WatchlistManager
):
    while True:
        try:
            # 1. Refesh watchlist from Data Service
            symbols = await data_service_client.get_intraday_watchlist()
            watchlist_manager.update(symbols)
            
            # 2. Fetch and publish latest data bar for each symbol

            for symbol in watchlist_manager.symbols:
                bar = await fetch_latest_1m_bar(symbol)
                if bar:
                    await publisher.publish(bar)

        except Exception as e:
            logger.exception(f"Error in market data loop {e}")

        await asyncio.sleep(settings.poll_interval_seconds)