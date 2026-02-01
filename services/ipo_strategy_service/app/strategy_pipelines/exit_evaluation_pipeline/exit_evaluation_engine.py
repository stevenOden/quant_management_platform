from datetime import datetime

# from sqlalchemy.ext.asyncio import AsyncSession
# from app.db import get_async_session
from sqlmodel import Session, select
from app.db import engine

from app.enums.ipo_state import IPOState
from app.strategy_pipelines.exit_evaluation_pipeline.exit_evaluation_logic import ExitLogic, HoldingSnapshot
from app.models.ipo_event import IPOEvent
from app.clients.execution_service_client import ExecutionServiceClient
from app.clients.data_service_client import DataServiceClient

import logging


class ExitEvaluationEngine:
    def __init__(self,exit_logic: ExitLogic, execution_client: ExecutionServiceClient):
        self.exit_logic = exit_logic
        self.execution_client = execution_client

    async def handle_price_tick(self, symbol: str, price: float, timestamp: str, data_service_client: DataServiceClient) -> None:
        ''' If we are holding this symbol evaluate the exit logic with the IPOEvent Data and the current price'''
        with Session(engine) as session:

            # 1. Query IPOEvent for the given symbol in state HOLDING
            ipo_event= session.exec(select(IPOEvent).where(IPOEvent.symbol == symbol,IPOEvent.state == IPOState.HOLDING)).first()

            if not ipo_event:
                return

            # 2. Isolate the data from IPOEvent into subset
            holding_data = HoldingSnapshot(
                symbol=ipo_event.symbol,
                quantity=ipo_event.position_num_share,
                entry_price=ipo_event.entry_price,
                stop_loss=ipo_event.stop_loss_price,
                take_profit=ipo_event.target_price
            )

            # 3. Evaluate the exit logic with the data subset and streamed price
            exit_signal = self.exit_logic.should_exit(holding_data,price)
            if not exit_signal:
                return

            # 4. If exit logic is valid, execute a sell order through the execution client connection
            execution_result = await self.execution_client.execute_trade(
                ipo_event.symbol,
                ipo_event.position_num_share,
                "SELL"
            )

            # 5. Record the last sell order data
            ipo_event.last_signal = exit_signal
            ipo_event.last_signal_at = datetime.fromisoformat(timestamp)
            ipo_event.exit_signal_price = price

            # 5. If the sell order was executed properly, record the execution data
            ipo_event.exit_price = execution_result.price # good for finding slippage
            ipo_event.exited_at = execution_result.timestamp
            ipo_event.state = IPOState.EXITED
            ipo_event.position_pnl = ipo_event.entry_price - ipo_event.exit_price

            # 6. Update the IntradayWatchlist to remove this symbol/strategy row
            intraday_watch = await data_service_client.remove_intraday_watchlist_symbol(symbol)
            if not intraday_watch:
                logging.warning(f"{symbol} could not be removed from the intraday watchlist")

            session.add(ipo_event)
            session.commit()
