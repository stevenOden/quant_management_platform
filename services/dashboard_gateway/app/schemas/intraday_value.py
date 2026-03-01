from pydantic import BaseModel
from datetime import datetime

class IntradayValue(BaseModel):
    timestamp: datetime
    portfolio_value: float

