import httpx
from app.config import EXECUTION_SERVICE_URL

class ExecutionClient:
    async def fetch_trade_history(self):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{EXECUTION_SERVICE_URL}/history")
            resp.raise_for_status()
            return resp.json()
