from fastapi import APIRouter, Depends
from app.schemas.strategy_state import StrategyState
from app.clients.strategy_client import StrategyClient

router = APIRouter()

@router.get("/states", response_model=list[StrategyState])
async def get_strategy_states(client: StrategyClient = Depends()):
    data = await client.fetch_states()
    return [StrategyState(**s) for s in data]
