from requests import Session
from abc import ABC, abstractmethod
from DTOs.PriceDTO import PriceDTO

class BaseWebClient(ABC):
    def __init__(self, timeout: int = 10) -> None:
        self.session = Session()
        self.timeout = timeout

    def fetch_price_dto(self, url) -> PriceDTO:
        html = self._fetch(url)
        raw_data = self._parse(html)
        return self._build_dto(raw_data)

    def _fetch(self, url: str) -> str:
        """Shared unless a site needs special handling (e.g. Playwright)."""
        resp = self.session.get(url, timeout=self.timeout)
        resp.raise_for_status()
        return resp.text

    @abstractmethod
    def _parse(self, html: str) -> dict:
        """Site-specific: extract raw fields from HTML."""
        pass

    def _build_dto(self, raw_data: dict) -> PriceDTO:
        """Shared — Pydantic does the validation/coercion."""
        return PriceDTO(**raw_data)