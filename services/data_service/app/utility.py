from datetime import datetime, timedelta, date
from zoneinfo import ZoneInfo

# Get timezone info that is daylight savings time aware
eastern_time_zone = ZoneInfo("America/New_York")

market_close = datetime.now(eastern_time_zone).replace(hour=16, minute=0, second=0, microsecond=0) # market close is 4pm Eastern
market_close_plus1 = market_close + timedelta(hours=1)
market_open = datetime.now(eastern_time_zone).replace(hour=9, minute=0, second=0, microsecond=0) # market open is 9 am Eastern
market_open_plus1 = market_open + timedelta(hours=1)
tomorrow_open = market_open + timedelta(days=1)


def get_today_eastern_timezone() -> date:
    return datetime.now(eastern_time_zone).date()

def get_tomorrow_eastern_timezone():
    return get_today_eastern_timezone() + timedelta(days=1)

def get_yesterday_eastern_timezone():
    return get_today_eastern_timezone() - timedelta(days=1)

def get_time_eastern_timezone() -> datetime:
    return datetime.now(eastern_time_zone)
