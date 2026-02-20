import httpx
from app.config import PORTFOLIO_SERVICE_URL

class PortfolioClient:
    async def fetch_overview(self):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{PORTFOLIO_SERVICE_URL}/overview")
            resp.raise_for_status()
            return resp.json()

    async def fetch_positions(self):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{PORTFOLIO_SERVICE_URL}/positions")
            resp.raise_for_status()
            return resp.json()
