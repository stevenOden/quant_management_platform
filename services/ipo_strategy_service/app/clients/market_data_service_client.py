import json
import httpx
from typing import AsyncIterator, Dict

from app.config import MARKET_DATA_SERVICE_URL

class MarketDataServiceClient:
    def __init__(self):
        self.base_url = MARKET_DATA_SERVICE_URL

    async def stream_prices(self) -> AsyncIterator[Dict]:
        '''
        Yields Dicts like:
        {
            "symbol": "ABCD",
            "price": 12.34,
            "timestamp": "2026-01-01T15:30:00Z"
        '''

        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("GET", f"{self.base_url}/stream") as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if not line:
                        continue
                    try:
                        event = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    yield event
