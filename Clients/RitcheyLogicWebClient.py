import json
from Skus.RitcheyLogicSku import RitcheyLogicSkus, RitcheySku
from Clients.BaseWebClient import HtmlWebClient
from bs4 import BeautifulSoup
from datetime import date


class RitcheyWebClient(HtmlWebClient):
    def __init__(self, timeout: int = 10):
        super().__init__(timeout)

    def _parse(self, html_soup: BeautifulSoup, ritchey_sku: RitcheySku) -> dict:
        product_json = self._find_product_jsonld(html_soup)
        variant = self._find_variant(product_json, ritchey_sku.sku)
        current_price = float(variant["offers"]["price"])

        msrp_price, sale_price = self._resolve_prices(html_soup, current_price)

        return {
            "product_id": ritchey_sku.product_slug,
            "date": date.today(),
            "msrp_price": msrp_price,
            "sale_price": sale_price,
        }

    def _find_product_jsonld(self, html_soup: BeautifulSoup) -> dict:
        for script in html_soup.select('script[type="application/ld+json"]'):
            try:
                data = json.loads(script.string)
            except (json.JSONDecodeError, TypeError):
                continue
            if isinstance(data, dict) and data.get("@type") == "Product":
                return data
        raise Exception("Error: No Product JSON-LD block found on page.")

    def _find_variant(self, product_json: dict, sku: str) -> dict:
        if product_json.get("sku") == sku:
            return product_json
        for variant in product_json.get("isVariantOf", {}).get("hasVariant", []):
            if variant.get("sku") == sku:
                return variant
        raise Exception(f"Error: SKU {sku} not found among product variants.")

    def _resolve_prices(self, html_soup: BeautifulSoup, current_price: float) -> tuple[float, float | None]:
        previous_price_tag = html_soup.select_one('span[aria-label="Previous price"]')
        if previous_price_tag:
            msrp_price = self._to_float(previous_price_tag.get_text(strip=True))
            return msrp_price, current_price
        return current_price, None

    @staticmethod
    def _to_float(text: str) -> float:
        return float(text.lstrip("$").replace(",", ""))
