import httpx
import logging
from fastapi import HTTPException
from app.config import PORTFOLIO_SERVICE_URL

logger = logging.getLogger(__name__)

class PortfolioClient:
    async def fetch_overview(self):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{PORTFOLIO_SERVICE_URL}/valuation/overview")
                resp.raise_for_status()
                return resp.json()

        except httpx.RequestError:
            logger.error("Portfolio Service unavailable")
            raise HTTPException(status_code=503, detail="Portfolio Service unavailable")

    async def fetch_daily_pnl(self):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{PORTFOLIO_SERVICE_URL}/valuation/daily_pnl")
                resp.raise_for_status()
                return resp.json()
        except httpx.RequestError:
            logger.error("Portfolio Service unavailable")
            raise HTTPException(status_code=503, detail="Portfolio Service unavailable")

    async def fetch_intraday_pnl(self):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{PORTFOLIO_SERVICE_URL}/valuation/intraday_pnl")
                resp.raise_for_status()
                return resp.json()

        except httpx.RequestError:
            logger.error("Portfolio Service unavailable")
            raise HTTPException(status_code=503, detail="Portfolio Service unavailable")

    async def fetch_positions(self):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{PORTFOLIO_SERVICE_URL}/positions")
                resp.raise_for_status()
                return resp.json()

        except httpx.RequestError:
            logger.error("Portfolio Service unavailable")
            raise HTTPException(status_code=503, detail="Portfolio Service unavailable")

