from requests import Session
from abc import ABC, abstractmethod
from DTOs.PriceDTO import PriceDTO
from bs4 import BeautifulSoup

class BaseWebClient(ABC):
    def __init__(self, timeout: int = 10) -> None:
        self.session = Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0 ..."})
        self.timeout = timeout

    def fetch_price_dto(self, sku_item) -> PriceDTO:
        html_soup = self._fetch(sku_item.url)
        raw_data = self._parse(html_soup, sku_item)
        return self._build_dto(raw_data)

    def _fetch(self, url: str) -> BeautifulSoup:
        """Shared unless a site needs special handling (e.g. Playwright)."""
        resp = self.session.get(url, timeout=self.timeout)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        return soup

    @abstractmethod
    def _parse(self, html_soup: BeautifulSoup, sku_item) -> dict:
        """Site-specific: extract raw fields from HTML."""
        ...

    def _build_dto(self, raw_data: dict) -> PriceDTO:
        """Shared — Pydantic does the validation/coercion."""
        return PriceDTO(**raw_data)