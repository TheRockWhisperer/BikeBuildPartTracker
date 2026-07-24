from dataclasses import dataclass
from enum import Enum
from datetime import date
from concurrent.futures import ProcessPoolExecutor

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from .BaseWebClient import BaseWebClient, PriceDTO


@dataclass(frozen=True)
class MerlinCyclesProductSku:
    """A single sellable product from Full Speed Ahead."""
    product_slug: str

    @property
    def url(self) -> str:
        return f"https://www.merlincycles.com/en-us/{self.product_slug}.html"

    @property
    def product_name(self) -> str:
        return self.product_slug.replace('-', ' ')


class MerlinCyclesSkus(Enum):
    SHIMANO_105_MECHANICAL_GROUPSET = MerlinCyclesProductSku("shimano-105-r7120-disc-groupset-12-speed-298406")
    SHIMANO_105_DI2_GROUPSET = MerlinCyclesProductSku("shimano-105-r7170-di2-disc-groupset-12-speed-271682")
    SHIMANO_ULTEGRA_DI2_GROUPSET = MerlinCyclesProductSku("shimano-ultegra-r8170-di2-disc-groupset-12-speed-252965")


def _fetch_merlin_html(url: str, timeout_ms: int = 10000) -> str:
    """
    Module-level worker function — must stay at module level (not a method)
    so ProcessPoolExecutor can pickle it to send to the child process.

    Runs in its own OS process, which on Windows gets a fresh, unmodified
    asyncio event loop policy (Proactor by default) — sidestepping the
    Selector-loop-can't-spawn-subprocesses issue that shows up when Playwright
    is run inside a Jupyter kernel's thread or event loop.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page()
            page.goto(url, wait_until="networkidle")
            page.wait_for_selector("div.product-pricing", timeout=timeout_ms)
            return page.content()
        finally:
            browser.close()


class MerlinCyclesWebClient(BaseWebClient):
    def __init__(self, timeout: int = 10):
        super().__init__(timeout)

    def fetch_price_dto(self, sku_item: MerlinCyclesProductSku) -> PriceDTO:
        html_soup = self._fetch(sku_item.url)
        raw_data = self._parse(html_soup, sku_item)
        return self._build_dto(raw_data)

    def _fetch(self, url: str) -> BeautifulSoup:
        with ProcessPoolExecutor(max_workers=1) as executor:
            html = executor.submit(_fetch_merlin_html, url).result()
        return BeautifulSoup(html, "html.parser")

    def _parse(self, html_soup: BeautifulSoup, merlin_product_sku: MerlinCyclesProductSku) -> dict:
        msrp_price, sale_price = self._parse_html_price_prices(html_soup)
        return {
            "product_id": merlin_product_sku.product_slug,
            "name": merlin_product_sku.product_name,
            "date": date.today(),
            "msrp_price": msrp_price,
            "sale_price": sale_price,
        }

    def _parse_html_price_prices(self, html_soup: BeautifulSoup) -> tuple[float, float | None]:
        pricing = html_soup.select_one("div.product-pricing")
        if not pricing:
            raise Exception("Error: Product pricing container not found on page.")

        current_tag = pricing.select_one("div.merlin-price span.price")
        if not current_tag:
            raise Exception("Error: No current price could be found.")
        current_price = self._to_float(current_tag.get_text(strip=True))

        rrp_tag = pricing.select_one("div.product-savings span.rrp span.price")
        if rrp_tag:
            rrp_price = self._to_float(rrp_tag.get_text(strip=True))
            # RRP only counts as MSRP if it's actually higher (defensive,
            # in case of a data glitch where rrp == current)
            if rrp_price > current_price:
                return rrp_price, current_price

        return current_price, None

    @staticmethod
    def _to_float(text: str) -> float:
        return float(text.lstrip("$").replace(",", ""))