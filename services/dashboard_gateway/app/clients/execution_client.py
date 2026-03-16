import httpx
import logging
from fastapi import HTTPException
from app.config import EXECUTION_SERVICE_URL

logger = logging.getLogger(__name__)

class ExecutionClient:
    async def fetch_trade_history(self):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{EXECUTION_SERVICE_URL}/history")
                resp.raise_for_status()
                return resp.json()

        except httpx.RequestError:
            logger.error("Execution Service unavailable")
            raise HTTPException(status_code=503, detail="Execution Service unavailable")
