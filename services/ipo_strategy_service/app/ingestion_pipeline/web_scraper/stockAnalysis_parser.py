from bs4 import BeautifulSoup
from typing import List, Dict, Any

def clean(value: str):
    return value if value not in ("","-", "—") else None

def parse_stockanalysis_html(html: str) -> List[Dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")

    if not table:
        return []

    rows = table.find_all("tr")[1:] # skips header row

    events = []
    for row in rows:
        cols = [c.get_text(strip=True) for c in row.find_all("td")]
        if not cols or len(cols) < 9:
            continue

        ipo_date = cols[0]
        company_name = cols[2]
        if not ipo_date or not company_name: # skip row if these crucial pieces are missing
            continue

        event = {
            "ipo_date": ipo_date,
            "symbol": clean(cols[1]),
            "company_name": company_name,
            "exchange": clean(cols[3]),
            "price_range": clean(cols[4]),
            "shares_offered": clean(cols[5]),
            "deal_size": clean(cols[6]),
            "market_cap": clean(cols[7]),
            "revenue": clean(cols[8]),
            "raw": cols
        }

        events.append(event)

    return events