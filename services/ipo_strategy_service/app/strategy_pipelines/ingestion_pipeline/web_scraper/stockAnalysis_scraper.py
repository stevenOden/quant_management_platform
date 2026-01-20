import httpx
from typing import List, Dict, Any
from app.strategy_pipelines.ingestion_pipeline.web_scraper.base_scraper import BaseScraper
from app.strategy_pipelines.ingestion_pipeline.web_scraper.stockAnalysis_parser import parse_stockanalysis_html

WEB_URL = f"https://stockanalysis.com/ipos/calendar/"

class StockAnalysisScraper(BaseScraper):
    async def fetch_raw(self) -> str:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(WEB_URL)
            response.raise_for_status()
            return response.text

    async def parse(self, raw_html: str) -> List[Dict[str, Any]]:
        return parse_stockanalysis_html(raw_html)

    async def fetch(self) -> List[Dict[str, Any]]:
        """Convienence wrapper: fetch + parse"""
        raw = await self.fetch_raw()
        return await self.parse(raw)

if __name__ == "__main__":
    import asyncio
    async def main():
        scraper = StockAnalysisScraper()
        events = await scraper.fetch()

    asyncio.run(main())