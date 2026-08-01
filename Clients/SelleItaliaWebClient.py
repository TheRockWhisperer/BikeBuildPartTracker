from Clients.BaseWebClient import HtmlWebClient
from Skus.SelleItaliaSku import SelleItaliaSku
import re
import json
from datetime import date


class SelleItaliaWebClient(HtmlWebClient):
    _BCDATA_RE = re.compile(r"var\s+BCData\s*=\s*(\{.*?\});", re.DOTALL)

    def __init__(self, timeout=10):
        super().__init__(timeout)

    def _fetch(self, url: str) -> dict:
        resp = self.session.get(url, timeout=self.timeout)
        resp.raise_for_status()
        match = self._BCDATA_RE.search(resp.text)
        if not match:
            raise ValueError(f"Could not find BCData on page: {url}")
        return json.loads(match.group(1))

    def _parse(self, page_data: dict, selle_italia_sku: SelleItaliaSku) -> dict:
        price_data = page_data["product_attributes"]["price"]
        sale_price_val = price_data["with_tax"]["value"]
        non_sale = price_data.get("non_sale_price_with_tax")

        if non_sale and non_sale["value"] > sale_price_val:
            msrp_price, sale_price = non_sale["value"], sale_price_val
        else:
            msrp_price, sale_price = sale_price_val, None

        return {
            "product_id": selle_italia_sku.product_slug,
            "name": selle_italia_sku.product_name,
            "date": date.today(),
            "msrp_price": msrp_price,
            "sale_price": sale_price,
        }