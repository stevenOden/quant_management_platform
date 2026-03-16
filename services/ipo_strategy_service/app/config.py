import os

DATA_SERVICE_URL = os.getenv("DATA_SERVICE_URL","http://localhost:8001")
EXECUTION_SERVICE_URL = os.getenv("EXECUTION_SERVICE_URL","http://localhost:8003")
INTRADAY_STREAMING_SERVICE_URL = os.getenv("INTRADAY_STREAMING_SERVICE_URL","http://localhost:8004")