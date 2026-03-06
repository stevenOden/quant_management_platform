from fastapi import APIRouter, Depends
from app.schemas.trade_history import TradeHistory
from app.clients.execution_client import ExecutionClient


router = APIRouter()

@router.get("/history", response_model=list[TradeHistory])
async def get_trade_history(client: ExecutionClient = Depends()):
    data = await client.fetch_trade_history()
    return [TradeHistory(**t) for t in data]

