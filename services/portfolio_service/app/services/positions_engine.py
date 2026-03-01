from typing import List
from app.models.position import Position
from app.models.cash_balance import CashBalance
from app.models.realized_pnl import RealizedPnl
from app.models.realized_pnl_events import RealizedPnlEvents
from app.models.cash_balance_events import CashBalanceEvents
from app.schemas.position import TradeUpdate, PositionRead
from sqlmodel import Session, select
from app.config import STARTING_PORTFOLIO_VALUE, DATA_SERVICE_URL
from ..schemas.valuation import PositionValuation, PortfolioSummary
import httpx
from fastapi import HTTPException

from ..utility import get_time_eastern_timezone


async def get_all_positions(session:Session) -> List[Position]:
    positions = session.exec(select(Position)).all()
    return positions

async def get_cash_balance(session:Session) -> float:
    cash = session.exec(select(CashBalance)).one_or_none()
    if cash is None:
        cash = CashBalance(id=1, amount=1_000_000)
        session.add(cash)
        session.commit()

    return cash.amount

async def update_cash_balance(session:Session, trade) -> float:
    cash = session.exec(select(CashBalance)).one_or_none()
    if cash is None:
        cash = CashBalance(id=1, amount=1_000_000)
        session.add(cash)
        session.commit()

    trade_value = trade.quantity*trade.price

    if trade.side.upper()=="BUY":
        cash_after = cash.amount - trade_value
    else:
        cash_after = cash.amount + trade_value

    event = CashBalanceEvents(
        timestamp=get_time_eastern_timezone(),
        symbol=trade.symbol,
        quantity=trade.quantity,
        execution_price=trade.price,
        cash_before=cash.amount,
        cash_delta=trade_value,
        cash_after=cash_after,
        trade_id=trade.trade_id
    )
    session.add(event)
    cash.amount = cash_after
    session.add(cash)
    session.commit()

    return cash.amount

async def get_realized_pnl(session:Session) -> float:
    current_pnl = session.exec(select(RealizedPnl)).one_or_none()
    if current_pnl is None:
        current_pnl = RealizedPnl(id=1, amount=0)
        session.add(current_pnl)
        session.commit()

    return current_pnl.amount

async def update_realized_pnl(session:Session, trade, trade_pnl) -> float:
    current_pnl = session.exec(select(RealizedPnl)).one_or_none()
    if not current_pnl:
        current_pnl = RealizedPnl(id=1, amount=0)
        session.add(current_pnl)
        session.commit()
    pnl_after = current_pnl.amount + trade_pnl
    event = RealizedPnlEvents(
        timestamp=get_time_eastern_timezone(),
        symbol=trade.symbol,
        quantity=trade.quantity,
        execution_price=trade.price,
        pnl_before=current_pnl.amount,
        pnl_delta=trade_pnl,
        pnl_after=pnl_after,
        trade_id=trade.trade_id
    )
    session.add(event)
    current_pnl.amount = pnl_after
    session.add(current_pnl)
    session.commit()

    return current_pnl.amount


async def update_position_from_trade(session:Session, trade:TradeUpdate) -> PositionRead:
    position = session.exec(select(Position).where(Position.symbol == trade.symbol.upper())).first()

    # 0. Idempotency check (avoid duplicate portfolio updates)
    if position and position.last_trade_id == trade.trade_id:
        return position

    symbol = trade.symbol.upper()
    qty = trade.quantity
    price = trade.price
    side = trade.side.upper()
    trade_value = qty*price

    if position is None:
        if side == "BUY":
            position = Position(
                symbol=symbol,
                quantity=qty,
                average_cost=price
            )
            # Update the cash balance to reflect the cost to execute buy order
            current_cash_value = await update_cash_balance(session,trade)
        else:
            raise HTTPException(status_code=400, detail="Cannot SELL a non-existant position")

    else:
        current_value = position.quantity * position.average_cost

        if side == "BUY":
            new_value = current_value + qty * price
            new_quantity = position.quantity + qty
            position.average_cost = new_value / new_quantity
            position.quantity = new_quantity
            # Update the cash balance to reflect the cost to execute buy order
            current_cash_value = await update_cash_balance(session, trade)

        elif side == "SELL":
            new_quantity = position.quantity - qty
            position.quantity = new_quantity
            realized_pnl = trade_value - current_value
            if new_quantity == 0:
                position.average_cost = 0 # reset the cost if position is fully closed
            elif new_quantity < 0:
                raise HTTPException(status_code=400, detail="Cannot SELL more than the current position quantity")
            current_pnl = await update_realized_pnl(session,trade,realized_pnl)
            current_cash_value = await update_cash_balance(session, trade)
        else:
            raise HTTPException(status_code=400, detail="Unexpected side type")

    position.last_trade_id = trade.trade_id
    session.add(position)
    session.commit()
    session.refresh(position)

    return position

async def get_portfolio_summary(session):
    positions = await get_all_positions(session)

    valuations = []
    total_mv = 0
    total_unrealized_pnl = 0

    async with httpx.AsyncClient() as client: # create single async http client
        for pos in positions:
            r = await client.post(f"{DATA_SERVICE_URL}/prices/{pos.symbol}/fetch")
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