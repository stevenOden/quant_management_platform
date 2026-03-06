from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..db import get_session
from ..models.position import Position
from ..schemas.position import PositionCreate, PositionRead, TradeUpdate
from ..schemas.valuation import PositionValuation, PortfolioSummary
from app.services.positions_engine import get_all_positions, get_portfolio_summary, update_position_from_trade
import httpx

router = APIRouter(prefix="/portfolio", tags =["portfolio"])

@router.post("/positions", response_model=PositionRead)
def add_position(position: PositionCreate, session: Session = Depends(get_session)):
    db_pos = Position(**position.dict())
    session.add(db_pos)
    session.commit()
    session.refresh(db_pos)
    return db_pos

@router.get("/", response_model=PortfolioSummary)
async def get_portfolio(session: Session = Depends(get_session)):
    return await get_portfolio_summary(session)

@router.get("/positions", response_model=list[PositionRead])
async def read_position(session: Session = Depends(get_session)):
    return await get_all_positions(session)

@router.get("/positions/{symbol}", response_model=PositionRead)
def read_position(symbol: str, session: Session = Depends(get_session)):
    position = session.exec(select(Position).where(Position.symbol == symbol.upper())).first()
    if not position:
        raise HTTPException(status_code=404, detail="Postition not found")

    return position

@router.post("/positions/update", response_model = PositionRead)
async def update_position(trade:TradeUpdate, session: Session = Depends(get_session)):
    return await update_position_from_trade(session, trade)