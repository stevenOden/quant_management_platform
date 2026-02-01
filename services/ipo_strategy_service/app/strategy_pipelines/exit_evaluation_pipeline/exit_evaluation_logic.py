from dataclasses import dataclass
from typing import Dict

@dataclass
class HoldingSnapshot:
    symbol: str
    quantity: float
    entry_price: float
    stop_loss: float
    take_profit: float

class ExitLogic:
    def should_exit(self,position_data: HoldingSnapshot, current_price: float) -> str | None:
        ## DEBUG
        # current_price = round(position_data.take_profit + 10000.0)
        ## END_DEBUG
        if current_price <= position_data.stop_loss:
            return "STOP_LOSS"
        elif current_price >= position_data.take_profit:
            return "TAKE_PROFIT"
        return None