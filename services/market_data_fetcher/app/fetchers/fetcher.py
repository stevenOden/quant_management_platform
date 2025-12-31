import requests
from app.config import (
DATA_SERVICE_URL
)

def trigger_data_service_fetch(symbol:str):
    url = f"{DATA_SERVICE_URL}/prices/{symbol}/fetch"
    response = requests.post(url)
    response.raise_for_status()
    return response.json()
