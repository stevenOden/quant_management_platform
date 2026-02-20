from fastapi import APIRouter, Depends
from app.schemas.portfolio_overview import PortfolioOverview
from app.schemas.position import Position
from app.clients.portfolio_client import PortfolioClient

router = APIRouter()

@router.get("/overview", response_model=PortfolioOverview)
async def get_portfolio_overview(client: PortfolioClient = Depends()):
    data = await client.fetch_overview()
    return PortfolioOverview

@router.get("/positions", response_model=list[Position])
async def get_positions(client: PortfolioClient = Depends()):
    data = await client.fetch_positions()
    return [Position(**p) for p in data]