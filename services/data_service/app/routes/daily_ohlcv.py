from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from datetime import date

from app.db import get_session
from app.services.daily_ohlcv_store import (
    get_daily_ohlcv_for_symbol,
    get_all_daily_ohlcv_for_symbol, upsert_daily_ohlcv
)
from app.services.market_data_fetcher import fetch_ohlcv_for_date
from app.schemas.daily_ohlcv import DailyOHLCVResponse

router = APIRouter(prefix="/daily")

@router.get("/{symbol}/{day}", response_model = DailyOHLCVResponse)
def get_daily_ohlcv_for_date(
        symbol: str,
        day: date,
        session: Session = Depends(get_session)
):
    '''Return the daily OHLCV bar for a specific symbol and date'''
    row = get_daily_ohlcv_for_symbol(symbol,day,session)
    if not row:
        raise HTTPException(status_code=404, detail=f"Daily OHLCV data not found for {symbol} | {day}")
    return row

@router.get("/{symbol}",response_model = list[DailyOHLCVResponse])
def get_all_daily_ohlcv(
        symbol: str,
        session: Session = Depends(get_session)
):
    '''Return all daily ohlcv data for symbol'''
    rows = get_all_daily_ohlcv_for_symbol(symbol, session)
    if not rows:
        raise HTTPException(status_code=404, detail=f"Daily OHLCV data not found for {symbol}")

    return rows

@router.post("/fetch/{symbol}/{day}", response_model=DailyOHLCVResponse)
async def fetch_and_store_daily_ohlcv(
        symbol: str,
        day: date,
        session: Session = Depends(get_session)
):
    '''Fetch daily OHLCV for a specific date, upsert it into the DailyOHLCV table and return the stored row'''
    # 1. Fetch from yfinance
    ohlcv = fetch_ohlcv_for_date(symbol,day)
    if not ohlcv:
        raise HTTPException(
            status_code=404,
            detail = f"No OHLCV data available for {symbol} on {day}"
        )

    # 2. Store in DB
    stored = upsert_daily_ohlcv(
        session=session,
        symbol=symbol,
        day=day,
        open=ohlcv["open"],
        high=ohlcv["high"],
        low=ohlcv["low"],
        close=ohlcv["close"],
        volume=ohlcv["volume"]
    )
    session.commit()
    session.refresh(stored)

    return stored