from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseScraper(ABC):

    @abstractmethod
    async def fetch_raw(self) -> str:
        """Fetch raw HTML or text from the data source"""
        pass

    @abstractmethod
    async def parse(self, raw_html: str) -> List[Dict[str, Any]]:
        """Parse raw HTML into structured IPO event dictionaries"""
        pass

    async def fetch(self) -> List[Dict[str, Any]]:
        """Convienence wrapper: fetch + parse"""
        raw = await self.fetch_raw()
        return await self.parse(raw)