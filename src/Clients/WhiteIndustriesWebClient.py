from Skus.WhiteIndustriesSku import WhiteIndustriesSku
from Clients.BaseWebClient import HtmlWebClient
from bs4 import BeautifulSoup, Tag
from datetime import date


class WhiteIndustriesWebClient(HtmlWebClient):
    def __init__(self, timeout: int = 10):
        super().__init__(timeout)

    def _parse(self, html_soup: BeautifulSoup, wi_sku: WhiteIndustriesSku) -> dict[str, str | float]:
        msrp_price, sale_price = self._parse_html_price_prices(html_soup)
        return {
            "product_id": wi_sku.product_slug,
            "name": wi_sku.product_name,
            "date": date.today(),
            "msrp_price": msrp_price,
            "sale_price": sale_price,
        }

    def _parse_html_price_prices(self, html_soup: BeautifulSoup) -> tuple[float, float | None]:
        price_block = html_soup.select_one('div[data-block-name="woocommerce/product-price"]')
        if not price_block:
            raise Exception("Error: Product price block not found on page.")

        del_tag: Tag | None = price_block.select_one("del .woocommerce-Price-amount")
        ins_tag: Tag | None = price_block.select_one("ins .woocommerce-Price-amount")

        if del_tag and ins_tag:
            msrp_price = self._to_float(del_tag.get_text(strip=True))
            sale_price = self._to_float(ins_tag.get_text(strip=True))
        else:
            amount_tag: Tag | None = price_block.select_one(".woocommerce-Price-amount")
            if not amount_tag:
                raise Exception("Error: No MSRP or Sale price could be found.")
            msrp_price = self._to_float(amount_tag.get_text(strip=True))
            sale_price = None

        return msrp_price, sale_price

    @staticmethod
    def _to_float(text: str) -> float:
        return float(text.lstrip('$').replace(',', ''))