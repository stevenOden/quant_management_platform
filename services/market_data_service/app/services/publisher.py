from abc import ABC, abstractmethod
from app.models.intraday_bar import IntradayBar
import logging

logger = logging.getLogger(__name__)

class MarketDataPublisher(ABC):
    def __init__(self):
        self.subscribers = set()

    def register(self, queue):
        self.subscribers.add(queue)

    def unregister(self, queue):
        self.subscribers.discard(queue)

    @abstractmethod
    async def publish(self, bar: IntradayBar) -> None:
        ...

class LoggingMarketDataPublisher(MarketDataPublisher):
    async def publish(self, bar: IntradayBar):
        logger.info(
            f"Publish IntradayBar: {bar.symbol} @ {bar.timestamp} "
            f"o={bar.open} h={bar.high} l={bar.low} c={bar.close} v={bar.volume}"
        )

class StreamingMarketDataPublisher(MarketDataPublisher):
    async def publish(self, bar: IntradayBar):
        for q in list(self.subscribers):
            await q.put(bar)
            logger.info(
                f"Publish IntradayBar: {bar.symbol} @ {bar.timestamp} "
                f"o={bar.open} h={bar.high} l={bar.low} c={bar.close} v={bar.volume}"
            )

# Initialize this here to import into main.py as well as routes
publisher: MarketDataPublisher = StreamingMarketDataPublisher()