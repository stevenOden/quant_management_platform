import httpx
from app.schemas.universe import SymbolResponse

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