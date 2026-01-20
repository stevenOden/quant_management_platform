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
    def should_exit(self,position_data: HoldingSnapshot, current_price: float) -> bool:
        if current_price <= position_data.stop_loss or current_price >= position_data.take_profit:
            return True
        return False