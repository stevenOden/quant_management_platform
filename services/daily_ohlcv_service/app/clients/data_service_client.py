import time

import requests
import logging

from app.config import DATA_SERVICE_URL
logger=logging.getLogger(__name__)

def get_symbols_from_universe():
        response = requests.get(f"{DATA_SERVICE_URL}/universe/symbols")
        response.raise_for_status()
        return response.json()

def get_health_status():
        up = False
        while not up:
                try:
                        response = requests.get(f"{DATA_SERVICE_URL}/health")
                        response.raise_for_status()
                        if response.status_code == 200:
                                up = True
                                logger.info("Data Service is up, proceeding.")
                        else:
                                logger.info("Waiting for data service to be up..")
                                time.sleep(5)
                except:
                        logger.info("Waiting for data service to be up..")
                        time.sleep(5)
        return True