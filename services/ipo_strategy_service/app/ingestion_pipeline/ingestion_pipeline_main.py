import logging
from app.ingestion_pipeline.web_scraper.stockAnalysis_scraper import StockAnalysisScraper
from app.ingestion_pipeline.web_scraper.stockAnalysis_normalizer import normalize_stockanalysis_row
from app.ingestion_pipeline.upsert_ipo_events import upsert_ipo_events
logger = logging.getLogger(__name__)

async def run_ipo_ingestion_pipeline():
    """
    Orchestrates new IPO data ingestion pipeline
    1.Scrape and parse https://stockanalysis.com/ipos/calendar/ for raw ipo rows
    2.Normalize data
    3.Upsert into the database
    """
    logger.info("Started IPO Ingestion Pipeline")
    # 1. Scrape and Parse
    scraper = StockAnalysisScraper()
    raw_data_rows = await scraper.fetch()

    ## DEBUG
    raw_data_rows = [{
        "ipo_date": "Jan 02, 2026",
        "symbol": "PLAY",
        "company_name": "Dave and Busters",
        "exchange": "NASDAQ",
        "price_range": "$10.00",
        "shares_offered": "10M",
        "deal_size": "$10M",
        "market_cap": "$100M",
        "revenue": "100M",
        "raw": ""
    }]
    ## END DEBUG

    normalized = []
    # 2. Normalize raw data
    for row in raw_data_rows:
        clean_data = normalize_stockanalysis_row(row)
        if clean_data:
            normalized.append(clean_data)

    logger.info(f"Normalized {len(normalized)} IPO rows")

    # 3. Upsert (Update existing row data / insert new row)
    upsert_ipo_events(normalized)
    logger.info("IPO Ingestion Pipeline Completed")