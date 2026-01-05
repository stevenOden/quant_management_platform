import httpx

class DataServiceClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")

    async def get_intraday_watchlist(self) -> list[str]:
        url = f"{self.base_url}/intraday_watchlist/symbols"
        async with httpx.AsyncClient as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()