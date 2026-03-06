import httpx
from app.config import IPO_STRATEGY_URL

class IPOStrategyClient:
    async def fetch_ipo_events(self):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{IPO_STRATEGY_URL}/ipos/")
            resp.raise_for_status()
            return resp.json()
