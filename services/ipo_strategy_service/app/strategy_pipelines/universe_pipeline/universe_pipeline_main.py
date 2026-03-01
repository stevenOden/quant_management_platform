from app.clients.data_service_client import DataServiceClient
from sqlmodel import Session,select
from app.models.ipo_event import IPOEvent
from datetime import datetime, timezone
from app.enums.ipo_state import IPOState
from app.db import engine
import logging

data_service_client = DataServiceClient()

logger = logging.getLogger(__name__)

async def run_universe_pipeline():
    with Session(engine) as session:
        discovered_ipos = session.exec(
            select(IPOEvent).where(IPOEvent.state==IPOState.DISCOVERED)).all()

        for ipo in discovered_ipos:
            await data_service_client.register_symbol(ipo.symbol)
            ipo.state = IPOState.WATCHING
            ipo.watching_since = datetime.now(timezone.utc)

            session.add(ipo)
            logger.info(f"{ipo.symbol} Added to Data Service Symbol Universe.")

        session.commit()