from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db import get_session
from app.services.ipo_event_service import get_symbol, get_all_symbols, modify_symbol
from app.schemas.ipo_event import IPOEventResponse

router = APIRouter(prefix="/ipos", tags=["ipos"])

@router.get("/", response_model=list[IPOEventResponse])
def list_ipos(session: Session = Depends(get_session)):
    rows = get_all_symbols(session)
    result = [
        IPOEventResponse.model_validate(row)
        for row in rows
    ]
    return result

@router.get("/{symbol}", response_model=IPOEventResponse)
def get_ipo(symbol: str, session: Session = Depends(get_session)):
    row = get_symbol(symbol, session)
    return IPOEventResponse.model_validate(row)

## FOR DEBUGGING
@router.post("/{symbol}/modify", response_model=IPOEventResponse)
def modify_ipo(symbol: str, fieldname: str, fieldvalue: str, fieldtype: str, session: Session = Depends(get_session)):
    row = modify_symbol(symbol,fieldname,fieldvalue,fieldtype,session)
    return IPOEventResponse.model_validate(row)