from enum import Enum
from .BaseSku import BaseSku


class WhiteIndustriesSku(BaseSku):
    """A single sellable product on whiteind.com."""

    def __init__(self, product_slug: str) -> None:
        self.product_type = "wheelset"
        self.product_brand = "white_industries"
        self.product_slug = product_slug
        self.variant_id = 8

    @property
    def url(self) -> str:
        return f"https://www.whiteind.com/product/{self.product_slug}/"

    @property
    def product_name(self) -> str:
        return self.product_slug.replace('-', ' ')


class WhiteIndustriesProductSkus(WhiteIndustriesSku, Enum):
    CLD_ALUMINUM_700C_ROAD_WHEELS = "cld-aluminum-700c-road-wheels"