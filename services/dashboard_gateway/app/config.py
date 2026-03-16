import os

DATA_SERVICE_URL = os.getenv("DATA_SERVICE_URL","http://localhost:8001")
PORTFOLIO_SERVICE_URL = os.getenv("PORTFOLIO_SERVICE_URL","http://localhost:8002")
EXECUTION_SERVICE_URL = os.getenv("EXECUTION_SERVICE_URL","http://localhost:8003")
INTRADAY_STREAMING_SERVICE_URL = os.getenv("INTRADAY_STREAMING_SERVICE_URL","http://localhost:8004")
IPO_STRATEGY_SERVICE_URL = os.getenv("IPO_STRATEGY_SERVICE_URL","http://localhost:8010")
