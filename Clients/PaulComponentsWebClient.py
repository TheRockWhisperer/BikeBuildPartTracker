from Clients.BaseWebClient import HtmlWebClient
import html, json, re
from Skus.PaulComponentsSku import PaulCompSku
from datetime import date


class PaulCompWebClient(HtmlWebClient):
    _VARIATIONS_RE = re.compile(
        r'data-product_variations="([^"]*)"', re.DOTALL
    )

    def __init__(self, timeout=10):
        super().__init__(timeout)

    def _fetch(self, url: str) -> list[dict]:
        resp = self.session.get(url, timeout=self.timeout)
        resp.raise_for_status()
        match = self._VARIATIONS_RE.search(resp.text)
        if not match:
            raise ValueError(f"Could not find data-product_variations on page: {url}")
        # The attribute value is HTML-entity-escaped JSON (&quot; etc.)
        raw = html.unescape(match.group(1))
        return json.loads(raw)

    def _parse(self, variations: list[dict], paul_comp_sku: PaulCompSku) -> dict:
        variant = next(
            v for v in variations if v["variation_id"] == paul_comp_sku.variant_id
        )

        sale_price_val = float(variant["display_price"])
        regular_price_val = float(variant["display_regular_price"])

        if regular_price_val > sale_price_val:
            msrp_price, sale_price = regular_price_val, sale_price_val
        else:
            msrp_price, sale_price = sale_price_val, None

        return {
            "product_id": variant.get("sku", str(paul_comp_sku.variant_id)),
            "date": date.today(),
            "msrp_price": msrp_price,
            "sale_price": sale_price,
        }