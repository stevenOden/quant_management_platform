import httpx
from app.config import DATA_SERVICE_URL

class DataServiceClient:
    def __init__(self):
        self.base_url = DATA_SERVICE_URL

    async def get_intraday_watchlist(self, source: str | None = None) -> list[str]:
        url = f"{self.base_url}/intraday_watchlist/symbols"
        async with httpx.AsyncClient() as client:
            if source is None:
                response = await client.get(url)
            else:
                response = await client.get(url,params={"source":source})
            response.raise_for_status()
            return response.json()