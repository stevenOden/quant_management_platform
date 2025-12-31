from datetime import datetime, timezone, tzinfo
from typing import Optional, Dict, Any

def parse_date(value: str) -> Optional[datetime.date]:
    if not value:
        return None

    try:
        date_obj = datetime.strptime(value,"%b %d, %Y").date()
        utctime = datetime(date_obj.year, date_obj.month, date_obj.day, tzinfo=timezone.utc)
        return utctime
    except Exception as e:
        print(f"Cannot parse date: {value}: {e}")

def parse_money(value: Optional[str]) -> Optional[float]:
    """
    Convert str of format ('$150M', 5M, '$300K') into float dollar values

    """

    if not value:
        return None

    v = value.replace("$", "").replace(",", "").strip().upper()

    multiplier = 1
    if v.endswith("M"):
        multiplier = 1_000_000
        v = v[:-1]
    if v.endswith("B"):
        multiplier = 1_000_000_000
        v = v[:-1]
    if v.endswith("K"):
        multiplier = 1_000
        v = v[:-1]

    try:
        return float(v) * multiplier
    except ValueError:
        return None

def parse_shares(value: Optional[str]) -> Optional[int]:
    """
    Convert str of format ('$150M', 5M, '$300K') into integers
    """
    money_val = parse_money(value)
    return int(money_val) if money_val is not None else None

def parse_price_range(value: Optional[str]) -> (Optional[float], Optional[float]):
    """
    Converts "$15-$17" in (15.0, 17.0)
    """

    if not value:
        return None, None

    cleaned = value.replace("$", "").replace(",","").strip()
    prices = cleaned.replace("—","-").split("-")
    if len(prices) == 1:
        low = None
        high = prices[0]
        return low, float(high.strip())
    elif len(prices) == 2:
        low = prices[0]
        high = prices[1]
        try:
            return float(low.strip()), float(high.strip())
        except Exception as e:
            print(f"Cannot parse {value}: {e}")
            return None, None
    else:
        print(f"Cannot parse {value}: Too many price values to handle")
        return None, None

def normalize_stockanalysis_row(raw_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:

    company_name = raw_data.get("company_name","").strip()
    ipo_date_raw = raw_data.get("ipo_date", "").strip()

    if not company_name:
        return None

    ipo_date = parse_date(ipo_date_raw)
    if ipo_date is None:
        return None

    price_low, price_high = parse_price_range(raw_data.get("price_range",""))

    return{
        "ipo_date": ipo_date,
        "symbol": (raw_data.get("symbol") or "").strip().upper() or None,
        "company_name": company_name,
        "exchange": (raw_data.get("exchange") or "").strip().upper() or None,
        "price_low": price_low,
        "price_high": price_high,
        "shares_offered": parse_shares(raw_data.get("shares_offered", "")),
        "deal_size": parse_money(raw_data.get("deal_size", "")),
        "market_cap": parse_money(raw_data.get("market_cap", "")),
        "revenue": parse_money(raw_data.get("revenue", "")),
    }