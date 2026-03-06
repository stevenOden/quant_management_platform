from fastapi import APIRouter, Depends
from app.schemas.strategy_state import StrategyState, IPOStateResponse
from app.clients.ipo_strategy_client import IPOStrategyClient
from datetime import datetime,date

router = APIRouter()

@router.get("/ipo_events", response_model=IPOStateResponse)
async def get_ipo_event_data(client: IPOStrategyClient = Depends()):
    data = await client.fetch_ipo_events()
    output = IPOStateResponse(
        DISCOVERED = [],
        WATCHING = [],
        IPO_DAY = [],
        READY = [],
        BUY_SIGNAL = [],
        SELL_SIGNAL = [],
        HOLDING = [],
        EXITED = [],
        MISSED = []
    )
    for ipo in data:
        state_list = getattr(output,ipo['state'])
        state_list.append(
            StrategyState(
                symbol = ipo['symbol'],
                strategy = 'ipo_strategy',
                state = ipo['state'],
                ipo_date = datetime.strptime(ipo['ipo_date'],'%Y-%m-%dT%H:%M:%S').date(),
                entry_price = ipo['entry_price'],
                entry_value = ipo['position_entry_value'],
                target_price = ipo['target_price'],
                stop_loss = ipo['stop_loss_price'],
                pnl = ipo['position_pnl'],
                pnl_percent = round(ipo['position_pnl']/ipo['position_entry_value'] * 100,2) if ipo['position_pnl'] else 0.0,
                last_evaluated = ipo['last_signal_at'],
            )
        )
    return output
