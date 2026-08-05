from datetime import date
from enum import Enum


class SelleItaliaSku:
    """A single sellable variant on selleitalia.com."""

    def __init__(self, product_slug: str, option_values: dict):
        self.product_type = "saddle"
        self.product_brand = "selle_italia"
        self.product_slug = product_slug
        self.variant_id = None
        self.option_values = option_values

    @property
    def url(self) -> str:
        base = f"https://www.selleitalia.com/{self.product_slug}/"
        if self.option_values:
            query = "&".join(
                f"attribute[{opt_id}]={val_id}"
                for opt_id, val_id in self.option_values.items()
            )
            return f"{base}?{query}"
        return base

    @property
    def product_name(self) -> str:
        return self.product_slug.replace("-", " ")


class SelleItaliaProductSkus(SelleItaliaSku, Enum):
    SLR_BOOST_ENDURANCE_S3_BLACK = ("slr-boost-endurance-ti-316-superflow", {186: 224, 219: 264})
    SLR_BOOST_ENDURANCE_L3_BLACK = ("slr-boost-endurance-ti-316-superflow", {186: 225, 219: 264})
