from abc import ABC, abstractmethod
from app.models.intraday_bar import IntradayBar
import logging

logger = logging.getLogger(__name__)

class MarketDataPublisher(ABC):
    @abstractmethod
    async def publish(self, bar: IntradayBar) -> None:
        ...

class LoggingMarketDataPublisher(MarketDataPublisher):
    async def publish(self, bar: IntradayBar):
        logger.info(
            f"Publish IntradayBar: {bar.symbol} @ {bar.timestamp} "
            f"o={bar.open} h={bar.high} l={bar.low} c={bar.close} v={bar.volume}"
        )