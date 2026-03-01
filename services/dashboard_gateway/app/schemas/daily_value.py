from pydantic import BaseModel
from datetime import date

class DailyValue(BaseModel):
    datestamp: date
    portfolio_value: float

