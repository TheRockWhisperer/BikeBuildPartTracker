from requests import Session
from abc import ABC, abstractmethod
from DTOs.PriceDTO import PriceDTO
from bs4 import BeautifulSoup
from typing import TypeVar

TRaw = TypeVar("TRaw")  # BeautifulSoup for HTML, dict for JSON APIs


class BaseWebClient(ABC):
    def __init__(self, timeout: int = 10) -> None:
        self.session = Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0 ..."})
        self.timeout = timeout

    def fetch_price_dto(self, sku_item) -> PriceDTO:
        raw_resp: TRaw = self._fetch(sku_item.url)
        raw_data: dict = self._parse(raw_resp, sku_item)
        return self._build_dto(raw_data)

    @abstractmethod
    def _fetch(self, url: str) -> BeautifulSoup:
        """Fetch and return the raw payload in whatever shape this site needs."""
        ...

    @abstractmethod
    def _parse(self, raw: TRaw, sku_item) -> dict:
        """Site-specific: extract raw fields from HTML or JSON."""
        ...

    def _build_dto(self, raw_data: dict) -> PriceDTO:
        """Shared — Pydantic does the validation/coercion."""
        return PriceDTO(**raw_data)


class HtmlWebClient(BaseWebClient):
    def _fetch(self, url: str) -> BeautifulSoup:
        resp = self.session.get(url, timeout=self.timeout)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "html.parser")
