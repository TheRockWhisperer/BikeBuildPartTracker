import json
from dataclasses import dataclass
from enum import Enum
from datetime import date
from concurrent.futures import ProcessPoolExecutor

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

from .BaseWebClient import BaseWebClient, PriceDTO
from Skus.PerformanceBikesSku import PerformanceBikeProductSku, PerformanceBikeBundleSku

# NOTE on variant products: some listings (e.g. cranksets with multiple arm
# lengths) expose each variant as a distinct product id via a `?v=<id>`
# query param on the same URL — the price block below only reflects
# whichever variant the URL resolves to. Make sure PerformanceBikeProductSku.url
# includes the `v=` param for any product that has a variant selector
# (look for a `ul.variants` block in the page), or you'll silently always
# scrape whichever variant the bare URL defaults to.


def _fetch_performancebike_html(url: str, timeout_ms: int = 20000) -> str:
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
            # "domcontentloaded" rather than "networkidle": this site keeps a
            # lot of trackers running in the background after the initial
            # render (GTM, Exponea, Clarity, PayPal, Affirm, adbeacon), which
            # can keep the network "busy" well past when the actual price
            # content we need has already arrived — "networkidle" waiting on
            # that is what was causing the selector timeout.
            page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
            try:
                # Wait for either the rendered price table OR the JSON-LD
                # structured-data block, whichever appears first — the parser
                # already falls back to JSON-LD if the table selector comes up
                # empty (see _parse_html_price_prices), and JSON-LD sits in
                # <head> so it's typically available very early.
                page.wait_for_selector(
                    "div.price table.theprice, script[type='application/ld+json']",
                    timeout=timeout_ms,
                )
            except PlaywrightTimeoutError:
                # Neither showed up in time — return whatever content did
                # load. _parse_html_price_prices will raise a clear error if
                # there's genuinely nothing usable on the page, rather than
                # us masking that behind a generic Playwright timeout here.
                pass
            return page.content()
        finally:
            browser.close()


class PerformanceBikeWebClient(BaseWebClient):
    def __init__(self, timeout: int = 10):
        super().__init__(timeout)

    def fetch_price_dto(self, sku_item) -> PriceDTO:
        """Accepts either a single PerformanceBikeProductSku (one page, one
        price) or a PerformanceBikeBundleSku (multiple component pages,
        summed into one price)."""
        if isinstance(sku_item, PerformanceBikeBundleSku):
            return self._fetch_bundle_price_dto(sku_item)

        html_soup = self._fetch(sku_item.url)
        raw_data = self._parse(html_soup, sku_item)
        return self._build_dto(raw_data)

    def _fetch_bundle_price_dto(self, bundle_sku: PerformanceBikeBundleSku) -> PriceDTO:
        """Fetches every component's page separately (each component is a
        distinct product listing on the site) and sums the results into a
        single combined price. If ANY component is on sale, the summed sale
        total uses each component's sale price where available and falls
        back to that component's regular price otherwise — i.e. it's the
        real total you'd pay buying every component today, not a total of
        two independent "is this a deal" flags."""
        msrp_total = 0.0
        sale_total = 0.0
        any_component_on_sale = False

        for component in bundle_sku.components:
            html_soup = self._fetch(component.url)
            component_msrp, component_sale = self._parse_html_price_prices(html_soup)
            msrp_total += component_msrp
            if component_sale is not None:
                any_component_on_sale = True
                sale_total += component_sale
            else:
                sale_total += component_msrp

        raw_data = {
            "product_id": bundle_sku.product_slug,
            "date": date.today(),
            "msrp_price": msrp_total,
            "sale_price": sale_total if any_component_on_sale else None,
        }
        return self._build_dto(raw_data)

    def _fetch(self, url: str) -> BeautifulSoup:
        with ProcessPoolExecutor(max_workers=1) as executor:
            html = executor.submit(_fetch_performancebike_html, url).result()
        return BeautifulSoup(html, "html.parser")

    def _parse(self, html_soup: BeautifulSoup, sku_item: PerformanceBikeProductSku) -> dict:
        msrp_price, sale_price = self._parse_html_price_prices(html_soup)
        return {
            "product_id": sku_item.product_slug,
            "date": date.today(),
            "msrp_price": msrp_price,
            "sale_price": sale_price,
        }

    def _parse_html_price_prices(self, html_soup: BeautifulSoup) -> tuple[float, float | None]:
        # Main product price block, confirmed from live markup:
        #   <div class="price">
        #     <table role="presentation"><tbody>
        #       <tr class="theprice single-line"><th>Price:</th><td>$1,804.99</td></tr>
        #     </tbody></table>
        #   </div>
        #
        # This platform (AMain-powered: Performance Bicycle, Jenson USA, etc.)
        # uses a consistent sale-price convention elsewhere on the same page
        # (in the "Related/Also Purchased" product grids):
        #   <div class="price"><s>$44.49</s><br><span class="productSpecialPrice">$36.99</span></div>
        # i.e. a struck-through <s> original price + span.productSpecialPrice
        # for the discounted price. The item in this listing isn't on sale,
        # so this exact combination hasn't been observed on the *main*
        # price block yet — verify against a discounted product page if you
        # can find one. The JSON-LD fallback below is a safety net either way.
        price_table = html_soup.select_one("div.price table.theprice")
        if price_table:
            td = price_table.select_one("td")
            if td:
                special_tag = td.select_one("span.productSpecialPrice")
                struck_tag = td.select_one("s")

                if special_tag and struck_tag:
                    sale_price = self._to_float(special_tag.get_text(strip=True))
                    msrp_price = self._to_float(struck_tag.get_text(strip=True))
                    if msrp_price > sale_price:
                        return msrp_price, sale_price
                    return sale_price, None

                # No sale markup — plain price in the cell, e.g. "$1,804.99"
                text = td.get_text(strip=True)
                if text:
                    return self._to_float(text), None

        # Fallback: schema.org JSON-LD Product/Offer block, present on every
        # product page as structured data for SEO — very stable regardless
        # of front-end markup changes:
        #   {"@type":"Product", ..., "offers":{"@type":"Offer","price":1804.99, ...}}
        for script_tag in html_soup.select("script[type='application/ld+json']"):
            try:
                data = json.loads(script_tag.string or "")
            except (json.JSONDecodeError, TypeError):
                continue
            entries = data if isinstance(data, list) else [data]
            for entry in entries:
                if isinstance(entry, dict) and entry.get("@type") == "Product":
                    offer = entry.get("offers") or {}
                    price = offer.get("price")
                    if price is not None:
                        return float(price), None

        raise Exception("Error: Product pricing container not found on page.")

    @staticmethod
    def _to_float(text: str) -> float:
        return float(text.lstrip("$").replace(",", ""))


def dump_pricing_html(url: str, out_path: str = "pricing_debug.html", timeout_ms: int = 10000) -> None:
    """
    One-off debug helper — NOT used in the scraping pipeline.

    Selectors in this file are confirmed against a live (non-sale) product
    page. If you want to double-check the sale-price branch (span.productSpecialPrice
    + <s> struck-through price) against the *main* product price block rather
    than just the related-items grids, run this against a discounted product
    once and grep the output for "productSpecialPrice".

        python -c "from PerformanceBikeWebClient import dump_pricing_html as d; \
            d('https://www.performancebike.com/.../pXXXXXXX')"
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page()
            page.goto(url, wait_until="networkidle")
            page.wait_for_timeout(2000)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(page.content())
            print(f"Saved rendered HTML to {out_path}")
        finally:
            browser.close()