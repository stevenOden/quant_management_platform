import requests
from app.config import DATA_SERVICE_URL

def get_symbols_from_universe():
        response = requests.get(f"{DATA_SERVICE_URL}/universe/symbols")
        response.raise_for_status()
        return response.json()
