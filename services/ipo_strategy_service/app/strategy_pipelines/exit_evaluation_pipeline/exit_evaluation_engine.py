from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.ipo_state import IPOState
from app.strategy_pipelines.exit_evaluation_pipeline.exit_evaluation_logic import ExitLogic, HoldingSnapshot
from app.models.ipo_event import IPOEvent
from app.clients.execution_service_client import ExecutionServiceClient

from app.db import async_session

class ExitEvaluationEngine:
    def __init__(self,exit_logic: ExitLogic, execution_client: ExecutionServiceClient):
        self.exit_logic = exit_logic
        self.execution_client = execution_client
    async def _get_holding_for_symbol(self, db: AsyncSession, symbol: str) -> IPOEvent | None:
        result = await db.execute(
            IPOEvent.__table__.select().where(
                IPOEvent.symbol == symbol,
                IPOEvent.state == IPOEvent.HOLDING
            )
        )

        row = result.first()
        if not row:
            return None
        return IPOEvent(**row._asdict()) if not isinstance(row,IPOEvent) else row

    async def handle_price_tick(self, symbol: str, price: float, timestamp: str) -> None:
        async with async_session() as db:
            ipo_event = await self._get_holding_for_symbol(db, symbol)
            if not ipo_event:
                return
            holding_data = HoldingSnapshot(
                symbol=ipo_event.symbol,
                quantity=ipo_event.position_num_share,
                entry_price=ipo_event.entry_price,
                stop_loss=ipo_event.stop_loss_price,
                take_profit=ipo_event.target_price
            )

            if not self.exit_logic.should_exit(holding_data,price):
                return
            # 1. Trigger sell through execution service
            execution_result = await self.execution_client.execute_trade(
                ipo_event.symbol,
                ipo_event.position_num_share,
                "SELL"
            )
            ipo_event.last_signal = "SELL"
            ipo_event.last_signal_at = timestamp
            ipo_event.exit_signal_price = price

            ipo_event.exit_price = execution_result.price # good for finding slippage
            ipo_event.exited_at = execution_result.timestamp
            ipo_event.state = IPOState.EXITED
            # TODO - partial fills?

            db.add(ipo_event)
            await db.commit()