import httpx
from app.config import IPO_STRATEGY_URL

class StrategyClient:
    async def fetch_states(self):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{IPO_STRATEGY_URL}/states")
            resp.raise_for_status()
            return resp.json()
