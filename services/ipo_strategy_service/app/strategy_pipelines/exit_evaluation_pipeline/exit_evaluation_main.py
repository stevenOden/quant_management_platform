from sqlmodel import Session, select
from app.db import engine
from app.models.ipo_event import IPOEvent
from app.enums.ipo_state import IPOState
from app.clients.market_data_service_client import MarketDataServiceClient
from app.clients.data_service_client import DataServiceClient
from app.clients.execution_service_client import ExecutionServiceClient
from app.strategy_pipelines.entry_evaluation_pipeline.entry_evaluation_pipeline_main import data_service_client
from app.strategy_pipelines.exit_evaluation_pipeline.exit_evaluation_logic import ExitLogic
from app.strategy_pipelines.exit_evaluation_pipeline.exit_evaluation_engine import ExitEvaluationEngine

async def run_exit_evaluation_pipeline():
    '''Evaluate non-signal generating time based state transitions and data collection'''

    # 1. Initialize the connection clients
    market_data_service_client = MarketDataServiceClient()
    execution_service_client = ExecutionServiceClient()
    data_service_client = DataServiceClient()

    # 2. Initialize the rules for exiting
    exit_logic = ExitLogic()

    # 3. Initialize the evaluation engine with the exit rules and the connection to the execution service
    exit_engine = ExitEvaluationEngine(exit_logic,execution_service_client)

    # 4. Stream intraday data from the market data service and iterte through each symbol
    async for event in market_data_service_client.stream_prices():
        symbol = event.get("symbol")
        price = event.get("close")
        timestamp = event.get("timestamp")

        if not symbol or price is None:
            continue

        # 5. Evaluate the exit logic and generate exit order if appropriate
        await exit_engine.handle_price_tick(symbol,price,timestamp, data_service_client)