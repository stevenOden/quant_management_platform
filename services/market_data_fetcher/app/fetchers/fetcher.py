import requests
from app.config import (
DATA_SERVICE_URL
)
from datetime import date

def trigger_data_service_fetch(symbol:str):
    url = f"{DATA_SERVICE_URL}/prices/{symbol}/fetch"
    response = requests.post(url)
    response.raise_for_status()
    return response.json()

def trigger_data_service_ohlcv_fetch(symbol:str,day:date):
    url = f"{DATA_SERVICE_URL}/daily/fetch/{symbol}/{day}"
    response = requests.post(url)
    response.raise_for_status()
    return response.json
