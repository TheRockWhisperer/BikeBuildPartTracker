from datetime import date
from Skus.BaseSku import BaseSku
from Clients.BaseWebClient import HtmlWebClient


class ShopifyWebClient(HtmlWebClient):
    def _fetch(self, url: str) -> dict:
        resp = self.session.get(url, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def _parse(self, product_json: dict, product_sku: BaseSku) -> dict:
            variants = product_json["product"]["variants"]
            variant = next(v for v in variants if v["id"] == product_sku.variant_id)
            
            price = float(variant["price"])
            compare_at = variant.get("compare_at_price")
            
            if compare_at and float(compare_at) > price:
                msrp_price, sale_price = float(compare_at), price
            else:
                msrp_price, sale_price = price, None
            
            return {
                "product_id": product_sku.product_slug,
                "date": date.today(),
                "msrp_price": msrp_price,
                "sale_price": sale_price,
            }
