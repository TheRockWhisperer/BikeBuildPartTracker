
from datetime import date
import re
from bs4 import BeautifulSoup, Tag
from Clients.BaseWebClient import HtmlWebClient
from Skus.SupacazSku import SupacazProductSku


class SupacazWebClient(HtmlWebClient):
    PRICE_BLOCK_SELECTOR = ".elementor-widget-woocommerce-product-price p.price"

    def __init__(self, timeout: int = 10):
            super().__init__(timeout)

    def _parse(self, html_soup: BeautifulSoup, sku: SupacazProductSku) -> dict[str, str | float]:
        msrp_price, sale_price = self._parse_html_price_prices(html_soup)
        return {
            "product_id": sku.product_slug,
            "name": sku.product_name,
            "date": date.today(),
            "msrp_price": msrp_price,
            "sale_price": sale_price,
        }

    def _parse_html_price_prices(self, html_soup: BeautifulSoup) -> tuple[float, float | None]:
        price_block = html_soup.select_one(self.PRICE_BLOCK_SELECTOR)
        if not price_block:
            # Fall back to a bare p.price in case the theme swaps the Elementor widget out
            price_block = html_soup.select_one("p.price")
        if not price_block:
            raise Exception("Error: Product price block not found on page.")

        del_tag: Tag | None = price_block.select_one("del .woocommerce-Price-amount")
        ins_tag: Tag | None = price_block.select_one("ins .woocommerce-Price-amount")

        if del_tag and ins_tag:
            return self._to_float(del_tag.get_text()), self._to_float(ins_tag.get_text())

        amounts = price_block.select(".woocommerce-Price-amount")
        if not amounts:
            raise Exception("Error: No MSRP or Sale price could be found.")

        if len(amounts) > 1:
            # Variable product renders a range, e.g. "$45.00 – $50.00"
            raise Exception(
                f"Error: Price is a range ({len(amounts)} amounts found); "
                "this product likely has variations and needs a variation-aware parser."
            )

        return self._to_float(amounts[0].get_text()), None

    @staticmethod
    def _to_float(text: str) -> float:
        cleaned = re.sub(r"[^\d.]", "", text)
        if not cleaned:
            raise ValueError(f"Could not parse a price from {text!r}")
        return float(cleaned)