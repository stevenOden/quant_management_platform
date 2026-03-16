import os

DATA_SERVICE_URL = os.getenv("DATA_SERVICE_URL","http://localhost:8001")
EXECUTION_SERVICE_URL = os.getenv("EXECUTION_SERVICE_URL","http://localhost:8003/execute")
STARTING_PORTFOLIO_VALUE = 1,000,000.00