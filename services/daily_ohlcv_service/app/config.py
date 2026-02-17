import os
from dotenv import load_dotenv

load_dotenv()

DATA_SERVICE_URL = os.getenv("DATA_SERVICE_URL", "http://localhost:8001")
FETCH_INTERVAL_SECONDS = int(os.getenv("FETCH_INTERVAL_SECONDS", 60))