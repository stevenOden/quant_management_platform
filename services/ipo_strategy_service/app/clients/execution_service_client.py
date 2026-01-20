import httpx
from datetime import date
from sqlmodel import Session
from app.schemas.trade_execution import Trade
from app.config import EXECUTION_SERVICE_URL

class ExecutionServiceClient:
    def __init__(self):
        self.base_url = EXECUTION_SERVICE_URL
    async def execute_trade(self, symbol: str, quantity: float, side: str ) -> Trade | None:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/execute/",
                json={"symbol":symbol, "quantity":quantity, "side":side},
                timeout=10.0
            )
            if response.status_code!= 200:
                return None
            response.raise_for_status()
            return Trade(**response.json())