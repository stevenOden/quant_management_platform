import httpx
from datetime import date
from sqlmodel import Session
from app.schemas.universe import SymbolResponse, IntradaySymbolResponse
from app.schemas.daily_ohlcv import DailyOHLCVResponse

class DataServiceClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
    async def register_symbol(self, symbol: str, source: str = "ipo_strategy") -> SymbolResponse:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/universe/symbols",
                json={"symbol":symbol, "source":source},
                timeout=10.0
            )
            response.raise_for_status()
            return SymbolResponse(**response.json())

    async def get_daily_ohlcv_data(self, symbol: str, date: date) -> DailyOHLCVResponse | None:
        url = f"{self.base_url}/daily/{symbol}/{date.isoformat()}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 404:
                return None
            return DailyOHLCVResponse(**response.json())

    async def get_current_price(self, symbol: str):
        url = f"{self.base_url}/prices/{symbol}/latest"
        with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 404:
                return None
            return response.json()['price']

    async def add_intraday_watchlist_symbol(self, symbol: str, source: str = "ipo_strategy"):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/intraday_watchlist/symbols/add",
                json={"symbol":symbol, "source":source},
                timeout=10.0
            )
            response.raise_for_status()
            return IntradaySymbolResponse(**response.json())

    async def remove_intraday_watchlist_symbol(self, symbol: str, source: str = "ipo_strategy"):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/intraday_watchlist/symbols/remove",
                json={"symbol":symbol, "source":source},
                timeout=10.0
            )
            response.raise_for_status()
            return IntradaySymbolResponse(**response.json())
