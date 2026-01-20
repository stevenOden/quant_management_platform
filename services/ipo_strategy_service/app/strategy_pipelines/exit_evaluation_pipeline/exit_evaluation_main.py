from sqlmodel import Session, select
from app.db import engine
from app.models.ipo_event import IPOEvent
from app.enums.ipo_state import IPOState
from app.clients.market_data_service_client import MarketDataServiceClient
from app.clients.data_service_client import DataServiceClient
from app.clients.execution_service_client import ExecutionServiceClient
from app.strategy_pipelines.exit_evaluation_pipeline.exit_evaluation_logic import ExitLogic
from app.strategy_pipelines.exit_evaluation_pipeline.exit_evaluation_engine import ExitEvaluationEngine

async def run_exit_evaluation_pipeline():
    '''Evaluate non-signal generating time based state transitions and data collection'''
    market_data_service_client = MarketDataServiceClient()
    execution_service_client = ExecutionServiceClient()
    exit_logic = ExitLogic()
    exit_engine = ExitEvaluationEngine(exit_logic,execution_service_client)

    # Iterate through each symbol
    async for event in market_data_service_client.stream_prices():
        symbol = event.get("symbol")
        price = event.get("price")
        timestamp = event.get("timestamp")

        if not symbol or price is None:
            continue

        # Handle the exit logic and
        await exit_engine.handle_price_tick(symbol,price,timestamp)