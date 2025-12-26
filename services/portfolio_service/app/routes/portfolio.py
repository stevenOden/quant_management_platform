from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..db import get_session
from ..models.position import Position
from ..schemas.position import PositionCreate, PositionRead, TradeUpdate
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

@router.post("/positions/update", response_model = PositionRead)
def update_position_from_trade(trade:TradeUpdate, session: Session = Depends(get_session)):
    position = session.exec(select(Position).where(Position.symbol == trade.symbol.upper())).first()

    symbol = trade.symbol.upper()
    qty = trade.quantity
    price = trade.price
    side = trade.side.upper()

    if position is None:
        if side == "BUY":
            position = Position(
                symbol=symbol,
                quantity=qty,
                average_cost=price
            )
        else:
            raise HTTPException(status_code=400, detail="Cannot SELL a non-existant position")

    else:
        current_value = position.quantity * position.average_cost

        if side == "BUY":
            new_value = current_value + qty * price
            new_quantity = position.quantity + qty
            position.average_cost = new_value / new_quantity
            position.quantity = new_quantity

        elif side == "SELL":
            new_quantity = position.quantity - qty
            position.quantity = new_quantity
            if new_quantity == 0:
                position.average_cost = 0 # reset the cost if position is fully closed
            elif new_quantity < 0:
                raise HTTPException(status_code=400, detail="Cannot SELL more than the current position quantity")
        else:
            raise HTTPException(status_code=400, detail="Unexpected side type")

    session.add(position)
    session.commit()
    session.refresh(position)

    return position