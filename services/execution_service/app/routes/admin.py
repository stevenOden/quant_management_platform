from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db import get_session
from app.models.trade import SystemState

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/clear_sync_flag")
def clear_sync_flag(session: Session = Depends(get_session)):
    '''Resets the portfolio_sync_required flag and is executed manually for safety'''
    state = session.get(SystemState, 1)
    if state is None:
        raise HTTPException(status_code=500, detail="SystemState row not found")
    state.portfolio_sync_required = False
    session.add(state)
    session.commit()

    return {"status": "SystemState Update Successful", "portfolio_sync_required": state.portfolio_sync_required}