from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..db import get_session
from ..models.position import Position
from ..schemas.position import PositionCreate, PositionRead
from ..schemas.valuation import PositionValuation, PortfolioSummary
import httpx

router = APIRouter()

DATA_SERVICE_URL = "http://localhost:8001/prices"

@router.post("/positions", response_model=PositionRead)
def add_position(position: PositionCreate, session: Session = Depends(get_session)):
    db_pos = Position(**position.dict())
    session.add(db_pos)
    session.commit()
    session.refresh(db_pos)
    return db_pos

@router.get("/", response_model=PortfolioSummary)
async def get_portfolio(session: Session = Depends(get_session)):
    positions = session.exec(select(Position)).all()

    valuations = []
    total_mv = 0
    total_unrealized_pnl = 0

    async with httpx.AsyncClient() as client: # create single async http client
        for pos in positions:
            r = await client.get(f"{DATA_SERVICE_URL}/{pos.symbol}/latest")
            latest_price = r.json()["price"]

            mv = pos.quantity * latest_price
            pnl = (latest_price - pos.average_cost) * pos.quantity

            total_mv += mv
            total_unrealized_pnl += pnl

            valuations.append(
                PositionValuation(
                    symbol=pos.symbol,
                    quantity=pos.quantity,
                    average_cost=pos.average_cost,
                    latest_price=latest_price,
                    market_value=mv,
                    unrealized_pnl=pnl,
                )
            )

    return PortfolioSummary(
        positions=valuations,
        total_market_value=total_mv,
        total_unrealized_pnl=total_unrealized_pnl,
    )

@router.get("/positions", response_model=list[PositionRead])
def read_position(session: Session = Depends(get_session)):
    positions = session.exec(select(Position)).all()
    return positions

@router.get("/positions/{symbol}", response_model=PositionRead)
def read_position(symbol: str, session: Session = Depends(get_session)):
    position = session.exec(select(Position).where(Position.symbol == symbol.upper())).first()
    if not position:
        raise HTTPException(status_code=404, detail="Postition not found")

    return position