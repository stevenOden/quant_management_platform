import httpx
import logging
from fastapi import HTTPException
from app.config import IPO_STRATEGY_SERVICE_URL

logger = logging.getLogger(__name__)

class IPOStrategyClient:
    async def fetch_ipo_events(self):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{IPO_STRATEGY_SERVICE_URL}/ipos/")
                resp.raise_for_status()
                return resp.json()

        except httpx.RequestError:
            logger.error("IPO Strategy Service unavailable")
            raise HTTPException(status_code=503, detail="IPO Strategy Service unavailable")